#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    MusaMusa-ETR Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-ETR.
#    MusaMusa-ETR is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-ETR is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-ETR.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
   MusaMusa-ETR project : musamusa_etr/etr.py

   ETR class

   (pimydoc)ETR format
   ⋅ -  utf8 encoded
   ⋅
   ⋅ -  empty lines        : lines made of spaces are discarded
   ⋅
   ⋅ -  comment lines      : lines starting with '#' are discarded
   ⋅
   ⋅                           → see ETR.parsingtools["comment_char"]
   ⋅
   ⋅ -  ⬂ character        : lines ending with ⬂ are joined to the next line
   ⋅                          with \n between the two lines.
   ⋅
   ⋅                           → see ETR.parsingtools["tobecontinued_char"]
   ⋅
   ⋅ -  left-spaces syntax : if True, lines beginning with spaces are joined
   ⋅                         to the precedent line with \n between the two lines.
   ⋅
   ⋅                           → see ETR.parsingtools["allow_leftspaces_syntax(json)"]
   ⋅
   ⋅ -  nested file        : +++ (=file to be included tag)
   ⋅                         the string after +++ will be stripped.
   ⋅
   ⋅                         it's a relative path based on the parent file,
   ⋅                         absolute path IS NOT allowed.
   ⋅                         e.g. if the file "directory/myfile.mus" contains the line
   ⋅                             +++ subdirectory/mynestedfile.mus
   ⋅                         the nested file will be directory/subdirectory/mynestedfile.mus
   ⋅
   ⋅                           → see ETR.parsingtools["filetobeincluded_tag"]
   ⋅
   ⋅  - abbreviations      :
   ⋅     :abbreviation: ᴺ  : [N]    # every "ᴺ" string will by replaced by "[N]"
   ⋅     :abbreviation: ᵛⁱ : [vi]   # every "ᵛⁱ" string will by replaced by "[vi]"
   ⋅
   ⋅                         Abbreviations are not applied to abbreviation, markers and flags.
   ⋅
   ⋅                         → see ETR.parsingtools["abbreviations_definitions regex"]
   ⋅
   ⋅ - flags:
   ⋅     :flag:            🏴‍☠️ : pirate  # the meaning of 🏴‍☠️ is 'pirate'
   ⋅
   ⋅                         → see ETR.parsingtools["flag_definitions regex"]
   ⋅
   ⋅ - marker:
   ⋅     :marker:          N            # you may use [N], {N} in text segments
   ⋅
   ⋅                         → see ETR.parsingtools["markers_definitions regex"]
   ⋅
   ⋅ - parsingtools definition:
   ⋅     %%tobecontinued_char%%
   ⋅
   ⋅                         → see ETR.parsingtools["parsingtools_definition(regex)"]

   ____________________________________________________________________________


   o ETR class
"""
import copy
from dataclasses import dataclass, field
import json
import os.path
import re
import traceback

from musamusa_errors.error_messages import ListOfErrorMessages, MusTextFileError
from musamusa_fal.fal import FileAndLine
from .utils import path_of


# (pimydoc)ETR.parsingtool
PARSINGTOOLS = {
        "comment_lineprefix": "#",
        "tobecontinued_char": "⬂",
        "allow_leftspaces_syntax(json)": True,
        "filetobeincluded_lineprefix": "+++",
        "category_kv(regex)": re.compile(r"^\:(?P<name>[^:]+)\:\s*"
                                         r"(?P<key>[^\s]*)\s*\:\s*(?P<value>[^\s]*)$"),
        "authorised categories(json)": ("abbreviation", "flag"),
        "parsingtools_definition(regex)": re.compile(r"%%(?P<name>[^:]+)%%(?P<value>.+)$"),
        }


@dataclass
class ETRLine:
    line: str
    fals: list = field(default_factory=list)
    flags: tuple = field(default_factory=tuple)


class ETR:

    def __init__(self,
                 parsingtools=None):
        """
            ETR.__init__()

            ___________________________________________________________________

            ARGUMENTS:
                o (None/dict)parsingtools, a dict of regexes and list of
                  chars allowing to detect markers in the source string.

                  Default parsingtools are defined in the PARSINGTOOLS variable.
                  See PARSINGTOOLS initialization to understant <parsingtools>
                  format.

                  About the <parsingtools> argument:
                    - by defaut, reasonable values are loaded
                    - you may want to set other parsingtools values by
                      setting <parsingtools> to a dict {...}.
        """
        self.errors = ListOfErrorMessages()

        # (pimydoc)ETR.parsingtools
        # ⋅ ETR.parsingtools is an attribute (NOT a class attribute).
        # ⋅ .parsingtools is a dict containing the following keys:
        # ⋅   * "comment_lineprefix"
        # ⋅     (str)line prefix defining a comment line
        # ⋅   * "tobecontinued_char"
        # ⋅     (str)character defining a to-be-continued line
        # ⋅   * "allow_leftspaces_syntax(json)" [JSON ! see below]
        # ⋅     a boolean allowing (or not) the left-spaces syntax
        # ⋅   * "filetobeincluded_lineprefix"
        # ⋅     (str)line prefix defining an import
        # ⋅   * "category(regex)" [REGEX ! see below]
        # ⋅     (str/bytes) regex defining a category key/value
        # ⋅     This regex must have the following groups:
        # ⋅         'name', 'key', 'value'
        # ⋅   * "authorised categories(json)" [JSON ! see below]
        # ⋅     (list of str) list of authorised categories
        # ⋅   * "parsingtools_definition(regex)" [JSON ! see below]
        # ⋅     Regex defining how modify the items of .parsingtools.
        # ⋅     This regex must have the following groups:
        # ⋅         'name', 'value'
        # ⋅
        # ⋅ If a key contains the "(regex)" suffix, its value must be (str)regex
        # ⋅ or a (byte)re.compile() object.
        # ⋅
        # ⋅ If a key contains the "(json)" suffix, its value is a Python object
        # ⋅ that can be read from a string through json.loads()
        if parsingtools:
            self.parsingtools = parsingtools
        else:
            self.parsingtools = {}
            self.initialize_parsingtools_with_reasonable_values()

        # self.read_categories[(str)name] = ((str)key, (str)value)
        # e.g. self.read_categories["abbreviation"] = ("e.g.", "exempli gratia")
        self.read_categories = {}

        # required to avoid cyclic imports:
        self._nested_files = []

    def _analyse_read_line(self,
                           line: str,
                           fals: FileAndLine):
        """
        TODO : returned value( None|str, None|tuple of str)
                RETURNED VALUE: None or str
                        None if the <line> doest not have to be yielded
                        (str)line otherwise

                (pimydoc)flags
                ⋅ Flags are sorted alphabetically via the sorted() function.

        """
        read_flags = []

        # ---- is there a new category definition ? ---------------------------
        cat = re.search(self.parsingtools["category_kv(regex)"],
                        line)
        if cat:
            if cat.group("name") in self.parsingtools["authorised categories(json)"]:

                if cat.group("name") not in self.read_categories:
                    self.read_categories[cat.group("name")] = {}

                if cat.group("key") in self.read_categories[cat.group("name")]:
                    # (pimydoc)error::ETR-ERRORID004
                    # ⋅ This error will be raised if a category is defined twice for the same key.
                    # ⋅
                    # ⋅ By example...
                    # ⋅   :abbreviation: ᵛⁱ : v+i
                    # ⋅   :abbreviation: ᵛⁱ : something else
                    # ⋅
                    # ⋅ ... raises an error since "ᵛⁱ" is defined twice as an abbreviation.
                    error = MusTextFileError()
                    error.msgid = "ETR-ERRORID004"
                    error.msg = f"({error.msgid}) Ill-formed file : " \
                        f"Duplicate category key '{cat.group('key')}'"
                    error.fals = fals
                    self.errors.append(error)
                else:
                    self.read_categories[cat.group("name")][cat.group("key")] = \
                        cat.group("value")
            else:
                # (pimydoc)error::ETR-ERRORID005
                # ⋅ This error will be raised if a category name is declared when it is not an
                # ⋅ authorized name.
                # ⋅
                # ⋅ By example, if .parsingtools["authorised categories(json)"] is
                # ⋅ ('abbreviation',), then
                # ⋅   :abbreviation: ᵛⁱ : something else
                # ⋅   :XYZ: ᵛⁱ          : v+i
                # ⋅
                # ⋅ ... raises an error since 'XYZ' isn't defined in
                # ⋅ .parsingtools["authorised categories(json)"].
                error = MusTextFileError()
                error.msgid = "ETR-ERRORID005"
                error.msg = f"({error.msgid}) Ill-formed file : " \
                    f"Unknown category name '{cat.group('name')}'; " \
                    "Authorized category names are: " \
                    f"{self.parsingtools['authorised categories(json)']}."
                error.fals = fals
                self.errors.append(error)

            # None since this <line> does not have to be yielded.
            return None, None

        # ---- is(are) there flag(s) ? ----------------------------------------
        if "flag" in self.read_categories:
            for flag_symbol, flag_value in self.read_categories["flag"].items():
                if flag_symbol in line:
                    line = line.replace(flag_symbol, "").strip()
                    read_flags.append(flag_value)

        # ---- is there abbreviation(s) to expand ? ---------------------------
        line = self._expand_abbrev(src=line)

        # ---- returned value -------------------------------------------------
        # (pimydoc)flags
        # ⋅ Flags are sorted alphabetically via the sorted() function.
        return (line.replace(self.parsingtools["tobecontinued_char"],
                             ""),
                tuple(sorted(read_flags)))

    def _expand_abbrev(self,
                       src: str) -> str:
        """
            ETR._expand_abbrev()

            Expand in <src> all abbreviations defined in self.parsingtools["abbreviations"]

            __________________________________________________________________

            o src : the string to be modified

            RETURNED VALUE : the modified string
        """
        if "abbreviation" not in self.read_categories:
            return src

        for before, after in sorted(self.read_categories["abbreviation"].items(),
                                    key=lambda item: len(item[0]),
                                    reverse=True):
            src = src.replace(before, after)
        return src

    def _read(self,
              source_filename,
              line_to_be_continued,
              next_line):
        """
            ETR._read()

            Subfunction of ETR.read()


            Iterator reading <source_filename> and yielding a list of
            ETRLine objects.

            Nested .mus files declared inside .mus files may be read through
            this method.
            __________________________________________________________________

            o source_filename      : (str) the path to the file to be read
            o next_line            : an ETRLine object.

            YIELDED VALUE : - either None if an error occured.
                            - either ETRLine
        """
        ptoo = self.parsingtools

        try:
            with open(source_filename,
                      encoding="utf-8") as content:

                line_index = 0
                for line_index, _line in enumerate(content):

                    # ---- is there a new "parsingtools_definition" ? ---------------------
                    ptooldef = re.search(self.parsingtools["parsingtools_definition(regex)"],
                                         _line)
                    if ptooldef:
                        if ptooldef.group("name") not in self.parsingtools:
                            # (pimydoc)error::ETR-ERRORID006
                            # ⋅ This error will be raised if a category name is declared in a
                            # ⋅ parsingtools_definition(regex) line when it is not an authorized
                            # ⋅ name.
                            # ⋅
                            # ⋅ The only authorized names are the keys of `.parsingtools` .
                            # ⋅
                            # ⋅ By example, with:
                            # ⋅
                            # ⋅  # this is a comment
                            # ⋅  %%XYZx%%|||
                            # ⋅
                            # ⋅  |||this a comment
                            # ⋅  Not a comment
                            # ⋅  # not a comment
                            # ⋅  A
                            # ⋅  B⏎
                            # ⋅
                            # ⋅ ... raises an error since "XYZx" isn't a key of .parsingtools .
                            error = MusTextFileError()
                            error.msgid = "ETR-ERRORID006"
                            error.msg = f"({error.msgid}) Ill-formed file : " \
                                "Illegal name for a " \
                                f"'parsingtools_definition(regex)' {ptooldef.group('name')}" \
                                f"Authorized names are {tuple(self.parsingtools.keys())}."
                            error.fals = (FileAndLine(filename=source_filename,
                                                      lineindex=line_index+1),)
                            self.errors.append(error)
                        else:
                            # (pimydoc)ETR.parsingtools
                            # ⋅ ETR.parsingtools is an attribute (NOT a class attribute).
                            # ⋅ .parsingtools is a dict containing the following keys:
                            # ⋅   * "comment_lineprefix"
                            # ⋅     (str)line prefix defining a comment line
                            # ⋅   * "tobecontinued_char"
                            # ⋅     (str)character defining a to-be-continued line
                            # ⋅   * "allow_leftspaces_syntax(json)" [JSON ! see below]
                            # ⋅     a boolean allowing (or not) the left-spaces syntax
                            # ⋅   * "filetobeincluded_lineprefix"
                            # ⋅     (str)line prefix defining an import
                            # ⋅   * "category(regex)" [REGEX ! see below]
                            # ⋅     (str/bytes) regex defining a category key/value
                            # ⋅     This regex must have the following groups:
                            # ⋅         'name', 'key', 'value'
                            # ⋅   * "authorised categories(json)" [JSON ! see below]
                            # ⋅     (list of str) list of authorised categories
                            # ⋅   * "parsingtools_definition(regex)" [JSON ! see below]
                            # ⋅     Regex defining how modify the items of .parsingtools.
                            # ⋅     This regex must have the following groups:
                            # ⋅         'name', 'value'
                            # ⋅
                            # ⋅ If a key contains the "(regex)" suffix, its value must be (str)regex
                            # ⋅ or a (byte)re.compile() object.
                            # ⋅
                            # ⋅ If a key contains the "(json)" suffix, its value is a Python object
                            # ⋅ that can be read from a string through json.loads()
                            if ptooldef.group("name").endswith("(regex)"):
                                try:
                                    self.parsingtools[ptooldef.group("name")] = \
                                       re.compile(ptooldef.group("value"))
                                except re.error as err:
                                    # (pimydoc)error::ETR-ERRORID007
                                    # ⋅ This error will be raised it's impossible to compile the
                                    # ⋅ regex defining a new parsingtools_definition.
                                    # ⋅
                                    # ⋅ By example, with:
                                    # ⋅   %%category_kv(regex)%%^\:?P<name>[^:]+)\:\s*(?P<key>[^\s]*)\s*\:\s*(?P<value>[^\s]*)$
                                    # ⋅
                                    # ⋅ An error will be raise since we should have:
                                    # ⋅     ^\:(?P<name>[^:]+)\...
                                    # ⋅ and not:
                                    # ⋅     ^\:?P<name>[^:]+)\...
                                    error = MusTextFileError()
                                    error.msgid = "ETR-ERRORID007"
                                    error.msg = f"({error.msgid}) Ill-formed file : " \
                                        f"can't interpret new parsingtools_definition. " \
                                        f"Can't compile regex {ptooldef.group('value')} " \
                                        f"Python error is '{err}' ."
                                    error.fals = (FileAndLine(filename=source_filename,
                                                              lineindex=line_index+1),)
                                    self.errors.append(error)
                            elif ptooldef.group("name").endswith("(json)"):
                                try:
                                    self.parsingtools[ptooldef.group("name")] = \
                                        json.loads(ptooldef.group("value"))
                                except json.decoder.JSONDecodeError as err:
                                    # (pimydoc)error::ETR-ERRORID008
                                    # ⋅ This error will be raised it's impossible to json-loads()
                                    # ⋅ the source string defining a json value.
                                    # ⋅
                                    # ⋅ By example, with:
                                    # ⋅   %%authorised categories(json)%%("abbreviation", "tag")
                                    # ⋅
                                    # ⋅ An error will be raise since we should have:
                                    # ⋅   %%authorised categories(json)%%["abbreviation", "tag"]
                                    # ⋅ and not:
                                    # ⋅   %%authorised categories(json)%%("abbreviation", "tag")
                                    error = MusTextFileError()
                                    error.msgid = "ETR-ERRORID008"
                                    error.msg = f"({error.msgid}) Ill-formed file : " \
                                        "can't interpret json string " \
                                        f"'{ptooldef.group('value')}'. " \
                                        f"Python error is '{err}' ."
                                    error.fals = (FileAndLine(filename=source_filename,
                                                              lineindex=line_index+1),)
                                    self.errors.append(error)
                            else:
                                self.parsingtools[ptooldef.group("name")] = ptooldef.group("value")
                        continue

                    # empty lines are ignored and comment lines are ignored:
                    if _line.strip() == "" or _line.startswith(ptoo["comment_lineprefix"]):
                        continue

                    # with the "left-spaces syntax" we have to preserve left-spaces string,
                    # hence the .rstrip() :
                    line = _line.rstrip() if ptoo["allow_leftspaces_syntax(json)"] \
                        else _line.strip()

                    # a special case : "left-spaces syntax" is enabled and <line> starts with
                    # a least one space:
                    if ptoo["allow_leftspaces_syntax(json)"] and line.startswith(" "):

                        # (pimydoc)error::ETR-ERRORID001
                        # ⋅ This error is raised if parsingtools["allow_leftspaces_syntax(json)"]
                        # ⋅ is True and if a line beginning with spaces can't joined to a
                        # ⋅ preceding line.
                        # ⋅
                        # ⋅ By example, trying to read such a file...
                        # ⋅
                        # ⋅ __B     (first line of the file, '_' is a space)
                        # ⋅ C
                        # ⋅ D       (last line of the file)
                        # ⋅
                        # ⋅ ...will raise this error.
                        if next_line is None:
                            error = MusTextFileError()
                            error.msgid = "ETR-ERRORID001"
                            error.msg = f"({error.msgid}) Ill-formed file : " \
                                "first line can't be added to a precedent line " \
                                "since the first character(s) of the first " \
                                "line are spaces " \
                                "and since <allow_leftspaces_syntax(json)> is True." \
                                f" line_index={line_index}"
                            error.fals = (FileAndLine(filename=source_filename,
                                                      lineindex=line_index+1),)
                            self.errors.append(error)
                        else:
                            # normal case : let's join <line> to the current <next_line>:
                            next_line.line += "\n" + line.strip()
                            next_line.fals.append(FileAndLine(filename=source_filename,
                                                              lineindex=line_index+1))
                            line_to_be_continued = line.endswith(ptoo["tobecontinued_char"])

                            continue

                    if _line.startswith(ptoo["filetobeincluded_lineprefix"]):
                        # recursive call to read a nested file:
                        new_fname = _line.removeprefix(ptoo["filetobeincluded_lineprefix"]).strip()
                        # new_fname = source_filename + new_fname
                        new_fname = os.path.join(path_of(source_filename), new_fname)

                        if next_line:
                            # we have to flush the current <next_line> before reading
                            # a nested file.
                            next_line.line, next_line.flags = self._analyse_read_line(
                                line=next_line.line,
                                fals=(FileAndLine(filename=source_filename,
                                                  lineindex=line_index+1),))
                            if next_line.line:  # may be None (see self._analyse_read_line())
                                yield ETRLine(
                                    fals=next_line.fals,
                                    flags=next_line.flags,
                                    line=next_line.line)
                            next_line = None

                        # recursive call to self.read():
                        yield from self.read(new_fname)
                        continue

                    # From now, the things go on without dealing with the "left-spaces syntax":
                    line = line.lstrip()

                    if line_to_be_continued:
                        # a special case : the current <next_line> (=the precedent line) was
                        # ended by ⬂:
                        next_line.line += "\n" + line
                        next_line.fals.append(FileAndLine(filename=source_filename,
                                                          lineindex=line_index+1))
                    else:
                        # normal case:
                        # we flush <next_line>:
                        if next_line:
                            next_line.line, next_line.flags = self._analyse_read_line(
                                line=next_line.line,
                                fals=(FileAndLine(filename=source_filename,
                                                  lineindex=line_index+1),))
                            if next_line.line:  # may be None (see self._analyse_read_line())
                                yield ETRLine(fals=next_line.fals,
                                              flags=next_line.flags,
                                              line=next_line.line)

                        # we have a new <next_line>:
                        next_line = ETRLine(fals=[FileAndLine(filename=source_filename,
                                                              lineindex=line_index+1), ],
                                            line=line)

                    # = does <line> end with ⬂ ?
                    line_to_be_continued = line.endswith(ptoo["tobecontinued_char"])

            # let's flush <next_line>:
            if next_line:
                next_line.line, next_line.flags = self._analyse_read_line(
                    line=next_line.line,
                    fals=(FileAndLine(filename=source_filename,
                                      lineindex=line_index+1),))
                if next_line.line:  # may be None (see self._analyse_read_line())
                    yield ETRLine(fals=next_line.fals,
                                  flags=next_line.flags,
                                  line=next_line.line)

                    # we have a new <next_line>:
                    _line2, _flags2 = self._analyse_read_line(
                        line=line,
                        fals=(FileAndLine(filename=source_filename,
                                          lineindex=line_index+1),))
                    if _line2:
                        next_line = ETRLine(fals=[FileAndLine(filename=source_filename,
                                                              lineindex=line_index+1), ],
                                            line=_line2,
                                            flags=_flags2)

        except KeyError:
            # (pimydoc)error::ETR-ERRORID003
            # ⋅ This error will be raised if `self.parsingtools` is wrongly modified during the
            # ⋅ reading loop.
            error = MusTextFileError()
            MusTextFileError.msgid = "ETR-ERRORID003"
            error.msg = f"({error.msgid}) Can't read '{source_filename}'. " \
                f"Python error is (KeyError)'{traceback.format_exc()}'."
            self.errors.append(error)

            yield None

    def initialize_parsingtools_with_reasonable_values(self):
        """
            ETR.initialize_parsingtools_with_reasonable_values()

            Wrapper around:
                self.parsingtools = copy.deepcopy(PARSINGTOOLS)

            (pimydoc)ETR.parsingtools
            ⋅ ETR.parsingtools is an attribute (NOT a class attribute).
            ⋅ .parsingtools is a dict containing the following keys:
            ⋅   * "comment_lineprefix"
            ⋅     (str)line prefix defining a comment line
            ⋅   * "tobecontinued_char"
            ⋅     (str)character defining a to-be-continued line
            ⋅   * "allow_leftspaces_syntax(json)" [JSON ! see below]
            ⋅     a boolean allowing (or not) the left-spaces syntax
            ⋅   * "filetobeincluded_lineprefix"
            ⋅     (str)line prefix defining an import
            ⋅   * "category(regex)" [REGEX ! see below]
            ⋅     (str/bytes) regex defining a category key/value
            ⋅     This regex must have the following groups:
            ⋅         'name', 'key', 'value'
            ⋅   * "authorised categories(json)" [JSON ! see below]
            ⋅     (list of str) list of authorised categories
            ⋅   * "parsingtools_definition(regex)" [JSON ! see below]
            ⋅     Regex defining how modify the items of .parsingtools.
            ⋅     This regex must have the following groups:
            ⋅         'name', 'value'
            ⋅
            ⋅ If a key contains the "(regex)" suffix, its value must be (str)regex
            ⋅ or a (byte)re.compile() object.
            ⋅
            ⋅ If a key contains the "(json)" suffix, its value is a Python object
            ⋅ that can be read from a string through json.loads()

            ___________________________________________________________________

            no RETURNED VALUE
        """
        self.parsingtools = copy.deepcopy(PARSINGTOOLS)

    def read(self,
             source_filename: str):
        """
            ETR.read()

                TODO

            ___________________________________________________________________

            no RETURNED VALUE
        """
        # (pimydoc)error::ETR-ERRORID002
        # ⋅ This error will be raised if a file F1 tries to import a file F2 and if F2
        # ⋅ has already import F1, maybe by means of several intermediate files.
        # ⋅
        # ⋅ By example, if F1 only contains the line:
        # ⋅ +++F2
        # ⋅ And if F2 only contains the line:
        # ⋅ +++F1
        # ⋅ ... this error will be raised.
        # ⋅
        # ⋅ By example, if F1 only contains the line:
        # ⋅ +++F2
        # ⋅ And if F2 only contains the line:
        # ⋅ +++F3
        # ⋅ And if F3 only contains the line:
        # ⋅ +++F1
        # ⋅ ... this error will be raised.
        if source_filename in self._nested_files:
            error = MusTextFileError()
            error.msgid = "ETR-ERRORID002"
            error.msg = f"({error.msgid}) " \
                f"Cyclic import in '{source_filename}' ." \
                f"Parent files already read are f{self._nested_files}"
            self.errors.append(error)
            yield None
            return

        self._nested_files.append(source_filename)

        # (pimydoc)error::ETR-ERRORID000
        # ⋅ Error raised if the source file to be read is missing.
        if not os.path.exists(source_filename):
            error = MusTextFileError()
            error.msgid = "ETR-ERRORID000"
            error.msg = f"({error.msgid}) " \
                f"Missing ETR MusaMusa text file '{source_filename}' ."
            self.errors.append(error)
            yield None
            return

        # main loop:
        yield from self._read(source_filename,
                              line_to_be_continued=False,
                              next_line=None)

        self._nested_files.pop()
