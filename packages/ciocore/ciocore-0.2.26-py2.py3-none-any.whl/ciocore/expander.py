
import os
import re
import hashlib
import base64
from string import Template
import abc

class AngleBracketTemplate(Template):
    """ Template for substituting tokens in angle brackets.

    Tokens may have mixed case letters and underscores.
    E.g. <foo>, <foo_bar> or <Scene>
    """
    delimiter = '<'
    pattern = r"""
    \<(?:
    (?P<escaped>\<)|
    (?P<named>  )\>|
    (?P<braced>[A-Za-z][A-Za-z_]+)\>|
    (?P<invalid>)
    )
    """


class Expander(object):
    """
    Class to expand angle bracket tokens and env vars.

    We handle tokens in strings, list values, and dict values (but not keys)
    """

    def __init__(self, safe=False, **context):
        self.context = context
        self._safe = safe

    def evaluate(self, target):
        """Evaluate target, whether its a value, list, or dict."""
        if type(target) == dict:
            result = {}
            for k in target:
                result[k] = self.evaluate_item(target[k])
            return result
        elif type(target) == list:
            return [self.evaluate_item(item) for item in target]
        return self.evaluate_item(target)

    def evaluate_item(self, item):
        """Evaluate an expression string

        Replace <token>s with values provided by the context dict
        """
        item = os.path.expandvars(item.strip())

        # run all expression resolvers
        context = self.context.copy()
        for resolver_class in ExpressionResolver.resolvers():
            resolver = resolver_class(item, context)
            item = resolver.template
            context = resolver.context
        # do the substitutions
        if self._safe:
            return AngleBracketTemplate(item).safe_substitute(context)
        try:
            return AngleBracketTemplate(item).substitute(context)
        except KeyError:
            raise KeyError("Invalid token. Valid tokens are: {}".format(
                self.context.keys()))
        except ValueError:
            raise ValueError("Invalid token. Valid tokens are: {}".format(
                self.context.keys()))

class ExpressionResolver(object):

    """
    Expression resolver base class.

    Templates may contain modifiers, such as for padding numbers or manipulating
    paths. Since the AngleBracketTemplate class (derived from Template) can't
    handle expressions, at least not in the customer friendly format we want, we
    have to resolve the expressions first, then modify the template and the
    context so they can be handed over to the AngleBracketTemplate to be
    resolved.

    Example: A template may contain "myfile.<pad framenumber 4>.exr" where
    context holds {"framenumber": 76}. Ultimately, we want to resolve to
    "myfile.0076.exr".

    To do this, we replace the expression token <pad framenumber 4> with a hash,
    like "<lJxKwmdZfi>" and we add that hash as a key in the context, and give
    it the resolved (modified) value of the variable: "0076".

    The modified context and template are accessed through public members of the
    same name.

    We handle as much as possible of the above in this base class so that
    derived classes may be minimal plugins and only concern themselves with
    specifying the expression format regex, and doing the actual modification.
    See: PadResolver and PosixResolver

.
    """
    __metaclass__ = abc.ABCMeta
    # must be overridden
    PATTERN = None

    @staticmethod
    def get_alpha_hash(rhs):
        """A 10 char hash of an expression string"""
        result = "".join([c for c in base64.b64encode(
            hashlib.md5(rhs).digest()) if c.isalpha()][:10])
        return result

    @classmethod
    def get_rx(cls):
        """Combine the regex from derived class with total template regex.

        The reason for this is so that we don't accidentally resolve patterns in
        escaped angle brackets. Admittedly, this is unlikely to ever happen.
        """
        rx = r"\<(?:(?P<escaped>\<)|(?P<named>)\>|(?P<braced>"
        rx += cls.PATTERN
        rx += r")\>|(?P<invalid>))"
        return re.compile(rx)

    @classmethod
    def resolvers(cls):
        """All the plugin classes"""
        return cls.__subclasses__()

    def __init__(self, template,  context):
        """Modify the template and context."""
        self.context = context.copy()
        self.template = template

        found = [x for x in self.get_rx().findall(template) if x[2]]
        # Will be something like [("","","pad frame 5",""),("","","pad endframe 4,"")]
        # Where each tuple captures an angle bracket token with an expression
        # that matches this plugin's regex.

        for group in found:
            expr = group[2]
            args = expr.split()
            # args[1] is the variable / i.e. the original context key
            if args[1] in self.context:
                key = self.get_alpha_hash(" ".join(args))

                # replace the expression in the template with the key (hash)
                self.template = self.template.replace(
                    "<{}>".format(expr), "<{}>".format(key))

                # add the new key to the context with the resolved value
                self.context[key] = self.resolve(*args[1:])

    @abc.abstractmethod
    def resolve(self):
        return


class PadResolver(ExpressionResolver):
    """
    Resolve padded number expressions
    """

    # A regex that describes the expression. For this padding function, we need
    # the word "pad", followed by the variable name, followed by a single digit.
    # e.g. pad framenumber 4
    PATTERN = r"pad\s+[A-Za-z][A-Za-z_]+\s+\d"

    def resolve(self, variable, *args):
        pad_value = int(args[0])
        var_value = int(self.context[variable])
        return "{{:0{}d}}".format(pad_value).format(var_value)

class PosixResolver(ExpressionResolver):
    """
    Resolve windows->posix path expressions
    """
    # A regex that describes the expression. For this path modifier, we need the word
    # "posix", followed by the variable name.
    # e.g. posix outpath
    PATTERN = r"posix\s+[A-Za-z][A-Za-z_]+"

    def resolve(self, variable):
        result = re.sub(r"^[a-zA-Z]:", "", self.context[variable] )
        return result.replace("\\", "/")


class UpperResolver(ExpressionResolver):
    """
    Resolve upper case expression
    """
    PATTERN = r"upper\s+[A-Za-z][A-Za-z_]+"

    def resolve(self, variable):
        return self.context[variable].upper()

class LowerResolver(ExpressionResolver):
    """
    Resolve lower case expression
    """
    PATTERN = r"lower\s+[A-Za-z][A-Za-z_]+"

    def resolve(self, variable):
        return self.context[variable].lower()


class BasenameResolver(ExpressionResolver):
    """
    Resolve basename expression.

    Can have optional x arg to denote strip_ext
    """
    PATTERN = r"basename\s+[A-Za-z][A-Za-z_]+"

    def resolve(self, variable, *args):
        return re.split("\\\\|/", self.context[variable])[-1]
        

class BasenamexResolver(ExpressionResolver):
    """
    Resolve basename expression.

    Can have optional x arg to denote strip_ext
    """
    PATTERN = r"basename_x\s+[A-Za-z][A-Za-z_]+"

    def resolve(self, variable, *args):
        base = re.split("\\\\|/", self.context[variable])[-1]
        return os.path.splitext(base)[0]

