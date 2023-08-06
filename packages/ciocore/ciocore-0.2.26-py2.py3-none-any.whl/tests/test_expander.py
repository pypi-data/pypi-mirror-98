
""" test sequence

   isort:skip_file
"""
import os
import sys
import unittest
import mock

SRC = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from ciocore.expander import (
    Expander, 
    PadResolver, 
    PosixResolver, 
    BasenameResolver, 
    BasenamexResolver)

class ExpanderTokensTest(unittest.TestCase):

    def setUp(self):
        self.context = {
            "Scene": "/projects/myscene",
            "RenderLayer": "masterLayer",
            "home": "/users/joebloggs/",
            "shot": "/metropolis/shot01/",
            "ct_dept": "texturing",
            "frames": 20,
            "directories": "/a/b /a/c"}

    def test_expand_value_target(self):
        e = Expander(**self.context)
        result = e.evaluate("x_<home>_y")
        self.assertEqual(result, "x_/users/joebloggs/_y")

    def test_expand_numeric_value_target(self):
        e = Expander(**self.context)
        result = e.evaluate("x_<frames>_y")
        self.assertEqual(result, "x_20_y")

    def test_expand_numeric_value_is_string(self):
        e = Expander(**self.context)
        result = e.evaluate("<frames>")
        self.assertIsInstance(result, str)
        self.assertEqual(result, "20")

    def test_bad_value_raises(self):
        e = Expander(**self.context)
        with self.assertRaises(KeyError):
            e.evaluate("<bad>")

    def test_mixed_case(self):
        e = Expander(**self.context)
        result = e.evaluate("x_<Scene>_y")
        self.assertEqual(result, "x_/projects/myscene_y")

    def test_repeated_tokens(self):
        e = Expander(**self.context)
        result = e.evaluate("x_<Scene>_<Scene>_y")
        self.assertEqual(result, "x_/projects/myscene_/projects/myscene_y")

    # lists
    def test_expand_list_target(self):
        e = Expander(**self.context)
        result = e.evaluate(["x_<shot>_y", "x_<ct_dept>_y"])
        self.assertIsInstance(result, list)
        self.assertEqual(result, ["x_/metropolis/shot01/_y", "x_texturing_y"])

    def test_expand_empty_list_target(self):
        e = Expander(**self.context)
        result = e.evaluate([])
        self.assertIsInstance(result, list)
        self.assertEqual(result, [])

    def test_bad_list_value_raises(self):
        e = Expander(**self.context)
        with self.assertRaises(KeyError):
            e.evaluate(["<bad>", "directories"])

    # dicts
    def test_expand_dict_target(self):
        e = Expander(**self.context)
        result = e.evaluate({"foo": "x_<shot>_y", "bar": "x_<ct_dept>_y"})
        self.assertIsInstance(result, dict)
        self.assertEqual(
            result, {"foo": "x_/metropolis/shot01/_y", "bar": "x_texturing_y"})

    def test_expand_empty_dict_target(self):
        e = Expander(**self.context)
        result = e.evaluate({})
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_bad_dict_value_raises(self):
        e = Expander(**self.context)
        with self.assertRaises(KeyError):
            e.evaluate({"foo": "<bad>", "bar": "directories"})

    def test_bad_dict_value_does_not_raise_if_safe(self):
        e = Expander(safe=True, **self.context)
        result = e.evaluate("x_<bad>_y")
        self.assertEqual(result, "x_<bad>_y")

    def test_strip(self):
        e = Expander(**self.context)
        result = e.evaluate(" x_<home>_y ")
        self.assertEqual(result, "x_/users/joebloggs/_y")


class ExpanderEnvVarTest(unittest.TestCase):

    def setUp(self):
        self.env = {
            "HOME": "/users/joebloggs",
            "SHOT": "MT_shot01",
            "DEPT": "texturing",
        }

    def test_expand_env_vars(self):
        with mock.patch.dict("os.environ", self.env):
            e = Expander()
            result = e.evaluate({"foo": "${SHOT}_hello", "bar": "x_${DEPT}_y"})
            self.assertIsInstance(result, dict)
            self.assertEqual(
                result, {"foo": "MT_shot01_hello", "bar": "x_texturing_y"})

    def test_doesnt_expand_nonexistent_vars(self):
        with mock.patch.dict("os.environ", self.env):
            e = Expander()
            o = {"foo": "${JOB}_hello", "bar": "x_${PROD}_y"}
            result = e.evaluate(o)
            self.assertIsInstance(result, dict)
            self.assertEqual(result, o)


class PadResolverTest(unittest.TestCase):

    def setUp(self):
        self.hash = PadResolver.get_alpha_hash("pad start 4")
        self.template = "<pad start 4>and<another expression>"
        self.context = {"start": 20, "Scene": "foo"}
        print self.hash

    def test_hashkey_in_template(self):
        r = PadResolver(self.template,  self.context)
        self.assertIn(self.hash, r.template)

    def test_hashkey_in_context(self):
        r = PadResolver(self.template,  self.context)
        self.assertIn(self.hash, r.context)

    def test_value_is_padded(self):
        r = PadResolver(self.template,  self.context)
        self.assertEqual(r.context[self.hash], "0020")

    def test_no_pad_leave_context_unchanged(self):
        r = PadResolver("<hui>",  self.context)
        self.assertEqual(r.context, self.context)

    def test_no_pad_leave_template_unchanged(self):
        r = PadResolver("<foo>_<pad>",  self.context)
        self.assertEqual(r.template, "<foo>_<pad>")

    def test_same_expression_with_different_spaces_creates_one_key(self):
        alphahash = PadResolver.get_alpha_hash("pad start 4")
        r = PadResolver("<pad start 4>and<pad   start    4>",  {"start": 20})
        self.assertEqual(r.template, "<{0}>and<{0}>".format(alphahash))


class PosixResolverTest(unittest.TestCase):

    def setUp(self):
        self.uncpath_hash = PosixResolver.get_alpha_hash("posix uncpath")
        self.letterpath_hash = PosixResolver.get_alpha_hash("posix letterpath")

        self.template = "<posix uncpath>and<posix letterpath>"
        self.context = {"start": 20, "uncpath": "\\\\a\\unc\\path",
                        "letterpath": "D:\\a\\letter\\path"}
        # print self.hash

    def test_hashkey_in_template(self):
        r = PosixResolver(self.template,  self.context)
        self.assertIn(self.uncpath_hash, r.template)
        self.assertIn(self.letterpath_hash, r.template)

    def test_hashkey_in_context(self):
        r = PosixResolver(self.template,  self.context)
        self.assertIn(self.uncpath_hash, r.context)
        self.assertIn(self.letterpath_hash, r.context)

    def test_unc_paths_are_converted(self):
        r = PosixResolver(self.template,  self.context)
        self.assertEqual(r.context[self.uncpath_hash], "//a/unc/path")

    def test_letter_paths_are_converted(self):
        r = PosixResolver(self.template,  self.context)
        self.assertEqual(r.context[self.letterpath_hash], "/a/letter/path")


class BasenameResolverTest(unittest.TestCase):

    def setUp(self):
        self.basename_hash = BasenameResolver.get_alpha_hash("basename patha")
        self.basename_x_hash = BasenameResolver.get_alpha_hash(
            "basename_x pathb")

        self.template = "<basename patha>and<basename_x pathb>"
        self.context = {
            "start": 20, 
            "patha": "D:\\a\\letter\\path\\file.exr", 
            "pathb": "/Users/foo/bar.ma"
            }

    def test_hashkey_in_template(self):
        r = BasenameResolver(self.template,  self.context)
        self.assertIn(self.basename_hash, r.template)

    def test_hashkey_in_template_x(self):
        r = BasenamexResolver(self.template,  self.context)
        self.assertIn(self.basename_x_hash, r.template)

    def test_hashkey_in_context(self):
        r = BasenameResolver(self.template,  self.context)
        self.assertIn(self.basename_hash, r.context)

    def test_hashkey_in_context_x(self):
        r = BasenamexResolver(self.template,  self.context)
        self.assertIn(self.basename_x_hash, r.context)

    def test_basename_path_converted(self):
        r = BasenameResolver(self.template,  self.context)
        self.assertEqual(r.context[self.basename_hash], "file.exr")

    def test_basename_x_path_converted(self):
        r = BasenamexResolver(self.template,  self.context)
        self.assertEqual(r.context[self.basename_x_hash], "bar")



class ExpanderWithExpressionTest(unittest.TestCase):

    def setUp(self):
        self.context = {"start": 20, "Scene": "foo"}

    def test_expand_value_with_expr(self):
        e = Expander(**self.context)
        result = e.evaluate("/prefix/<Scene>.<pad start 4>.exr")
        self.assertEqual(result, "/prefix/foo.0020.exr")

    def test_expand_value_with_several_plugins(self):
        e = Expander(start=20, outpath="C:\\my\\path")
        result = e.evaluate("<posix outpath>/foo.<pad start 4>.exr")
        self.assertEqual(result, "/my/path/foo.0020.exr")

    def test_expand_value_with_expr_when_appears_twice(self):
        e = Expander(**self.context)
        result = e.evaluate("/prefix/<pad start 6>/<Scene>.<pad start 4>.exr")
        self.assertEqual(result, "/prefix/000020/foo.0020.exr")

    def test_expand_value_with_expr_when_identical_expr_appears_twice(self):
        e = Expander(**self.context)
        result = e.evaluate("/prefix/<pad start 4>/<Scene>.<pad start 4>.exr")
        self.assertEqual(result, "/prefix/0020/foo.0020.exr")

    def test_invalid_when_expr_invalid(self):
        e = Expander(**self.context)
        with self.assertRaises(ValueError):
            e.evaluate("/prefix/<pad start X>/<Scene>.<pad start 4>.exr")


if __name__ == '__main__':
    unittest.main()
