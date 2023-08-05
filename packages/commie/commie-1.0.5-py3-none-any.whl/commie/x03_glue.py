# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo.werhal.com>
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from typing import *

from .x01_common import Comment


def _startsTheLine(text: str, pos: int) -> bool:
	"""Returns True if the line contains only blanks to
	the left to the pos"""

	prevNewLinePos = text.rfind("\n", 0, pos + 1)
	# if this is the first string, we'll get prevNewLinePos=-1.
	# But we still can get the followining substring:
	lineStart = text[prevNewLinePos + 1:pos]
	return not lineStart.strip()  # true if all blanks


class TestStartsTheLine(unittest.TestCase):

	def test_first_string(self):
		text = "   abc"
		self.assertEqual(_startsTheLine(text, text.find("a")), True)
		self.assertEqual(_startsTheLine(text, text.find("b")), False)

	def test_multi_string(self):
		text = """	abc
					12345
					def"""

		self.assertEqual(len(text.splitlines()), 3)

		self.assertEqual(_startsTheLine(text, text.find("a")), True)
		self.assertEqual(_startsTheLine(text, text.find("b")), False)
		self.assertEqual(_startsTheLine(text, text.find("c")), False)

		self.assertEqual(_startsTheLine(text, text.find("1")), True)
		self.assertEqual(_startsTheLine(text, text.find("2")), False)
		self.assertEqual(_startsTheLine(text, text.find("3")), False)
		self.assertEqual(_startsTheLine(text, text.find("4")), False)
		self.assertEqual(_startsTheLine(text, text.find("5")), False)

		self.assertEqual(_startsTheLine(text, text.find("d")), True)
		self.assertEqual(_startsTheLine(text, text.find("e")), False)
		self.assertEqual(_startsTheLine(text, text.find("f")), False)


def _oneEmptyLineBetween(text: str, start: int, end: int) -> bool:
	between = text[start:end]
	linesBetween = between.splitlines()
	return len(linesBetween) == 2 and not any(s.strip() for s in linesBetween)


def group_singleline_comments(comments: Iterable[Comment]) -> Iterable[List[Comment]]:
	"""Combines adjacent single-line comments into groups."""

	group: List[Comment] = []

	for comment in comments:

		if not comment.multiline and _startsTheLine(comment.source, comment.code_span.start):
			if group and not _oneEmptyLineBetween(comment.source, group[-1].code_span.end,
												  comment.code_span.start):
				if group:
					yield group
					group = []
			group.append(comment)
			continue

		if group:
			yield group
			group = []
		yield [comment]

	if group:
		yield group


class TestGlue(unittest.TestCase):

	def testEmpty(self):
		from .parsers import iter_comments_c
		source = ""
		groups = list(group_singleline_comments(iter_comments_c(source)))
		self.assertEqual(len(groups), 0)


	def testThreeSingleLines(self):
		from .parsers import iter_comments_c

		source = """
			// three single line
			// comments will be treated
			// as a single comment
		"""

		groups = list(group_singleline_comments(iter_comments_c(source)))

		self.assertEqual(len(groups), 1)
		self.assertEqual(len(groups[0]), 3)

	def testThreeSingleLinesTooMuchSpaces(self):
		from .parsers import iter_comments_c

		source = """
			// comment a
			
			// comment b
			
			
			// comment c
		"""

		groups = list(group_singleline_comments(iter_comments_c(source)))
		self.assertEqual(len(groups), 3)

	def testThreeMultiLines(self):
		from .parsers import iter_comments_c

		source = """
			/* comment a */
			/* comment b */
			/* comment c */
		"""

		groups = list(group_singleline_comments(iter_comments_c(source)))
		self.assertEqual(len(groups), 3)

	def testSSM(self):
		from .parsers import iter_comments_c

		source = """
			// comment a
			// comment b
			/* comment c */
		"""

		groups = list(group_singleline_comments(iter_comments_c(source)))
		self.assertEqual(len(groups), 2)
		self.assertEqual(len(groups[0]), 2)
		self.assertEqual(len(groups[1]), 1)

	def testMSS(self):
		from .parsers import iter_comments_c

		source = """
			/* comment a */
			// comment b
			// comment c
		"""

		groups = list(group_singleline_comments(iter_comments_c(source)))
		self.assertEqual(len(groups), 2)
		self.assertEqual(len(groups[0]), 1)
		self.assertEqual(len(groups[1]), 2)

	def testSMS(self):
		from .parsers import iter_comments_c

		source = """
			// comment a
			/* comment b */
			// comment c
		"""

		groups = list(group_singleline_comments(iter_comments_c(source)))
		self.assertEqual(len(groups), 3)

	def testMSM(self):
		from .parsers import iter_comments_c

		source = """
			/* comment a */
			// comment b
			/* comment c */
		"""

		groups = list(group_singleline_comments(iter_comments_c(source)))
		self.assertEqual(len(groups), 3)

	def testMix1(self):
		from .parsers import iter_comments_c

		source = """
			// first single comment
			#include<stdio.h>

			// three single line
			// comments will be treated
			// as a single comment

			void main() {
				// one more single comment
				print("bye!");
			}
		"""

		groups = list(group_singleline_comments(iter_comments_c(source)))

		for g in groups:
			print(len(g), g[0].text)

		self.assertEqual(len(groups), 3)
		self.assertEqual(len(groups[0]), 1)
		self.assertEqual(len(groups[1]), 3)
		self.assertEqual(len(groups[2]), 1)

	def testMix2(self):
		from .parsers import iter_comments_c

		source = """
			#include<stdio.h>

			// 0 three single line
			// 0 comments will be treated
			// 0 as a single comment
			
			// 1 single
			int x; // 2 one more single
			
			// 3 empty line above
			// 3 makes it easier

			void main() {
				print("bye!");
			}
		"""

		groups = list(group_singleline_comments(iter_comments_c(source)))

		self.assertEqual(len(groups), 4)
		self.assertEqual(len(groups[0]), 3)
		self.assertEqual(len(groups[1]), 1)
		self.assertEqual(len(groups[2]), 1)
		self.assertEqual(len(groups[3]), 2)

	def testMix3(self):
		from .parsers import iter_comments_c

		source = """
			#include<stdio.h>

			// 0 three single line
			// 0 comments will be treated
			// 0 as a single comment
			
			// 1 single
			int x; // 2 one more single
			// 3 no lines above
			// 3 but it's not glued to 2

			void main() {
				print("bye!");
			}
		"""

		groups = list(group_singleline_comments(iter_comments_c(source)))

		for g in groups:
			print(len(g))

		self.assertEqual(len(groups), 4)
		self.assertEqual(len(groups[0]), 3)
		self.assertEqual(len(groups[1]), 1)
		self.assertEqual(len(groups[2]), 1)
		self.assertEqual(len(groups[3]), 2)


if __name__ == "__main__":
	unittest.main()
