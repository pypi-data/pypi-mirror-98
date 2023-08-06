#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD.
# See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# All the space groups that GULP will print
sg = ['P 1             ','P -1            ','P 2             ','P 21            ',
      'C 2             ','P M             ','P C             ','C M             ','C C             ',
      'P 2/M           ','P 21/M          ','C 2/M           ','P 2/C           ','P 21/C          ',
      'C 2/C           ','P 2 2 2         ','P 2 2 21        ','P 21 21 2       ','P 21 21 21      ',
      'C 2 2 21        ','C 2 2 2         ','F 2 2 2         ','I 2 2 2         ','I 21 21 21      ',
      'P M M 2         ','P M C 21        ','P C C 2         ','P M A 2         ','P C A 21        ',
      'P N C 2         ','P M N 21        ','P B A 2         ','P N A 21        ','P N N 2         ',
      'C M M 2         ','C M C 21        ','C C C 2         ','A M M 2         ','A B M 2         ',
      'A M A 2         ','A B A 2         ','F M M 2         ','F D D 2         ','I M M 2         ',
      'I B A 2         ','I M A 2         ','P M M M         ','P N N N         ','P C C M         ',
      'P B A N         ','P M M A         ','P N N A         ','P M N A         ','P C C A         ',
      'P B A M         ','P C C N         ','P B C M         ','P N N M         ','P M M N         ',
      'P B C N         ','P B C A         ','P N M A         ','C M C M         ',
      'C M C A         ','C M M M         ','C C C M         ','C M M A         ','C C C A         ',
      'F M M M         ','F D D D         ','I M M M         ','I B A M         ','I B C A         ',
      'I M M A         ','P 4             ','P 41            ','P 42            ','P 43            ',
      'I 4             ','I 41            ','P -4            ','I -4            ','P 4/M           ',
      'P 42/M          ','P 4/N           ','P 42/N          ','I 4/M           ','I 41/A          ',
      'P 4 2 2         ','P 4 21 2        ','P 41 2 2        ','P 41 21 2       ','P 42 2 2        ',
      'P 42 21 2       ','P 43 2 2        ','P 43 21 2       ','I 4 2 2         ','I 41 2 2        ',
      'P 4 M M         ','P 4 B M         ','P 42 C M        ','P 42 N M        ','P 4 C C         ',
      'P 4 N C         ','P 42 M C        ','P 42 B C        ','I 4 M M         ','I 4 C M         ',
      'I 41 M D        ','I 41 C D        ','P -4 2 M        ','P -4 2 C        ','P -4 21 M       ',
      'P -4 21 C       ','P -4 M 2        ','P -4 C 2        ','P -4 B 2        ','P -4 N 2        ',
      'I -4 M 2        ','I -4 C 2        ','I -4 2 M        ','I -4 2 D        ',
      'P 4/M M M       ','P 4/M C C       ','P 4/N B M       ','P 4/N N C       ','P 4/M B M       ',
      'P 4/M N C       ','P 4/N M M       ','P 4/N C C       ','P 42/M M C      ','P 42/M C M      ',
      'P 42/N B C      ','P 42/N N M      ','P 42/M B C      ','P 42/M N M      ','P 42/N M C      ',
      'P 42/N C M      ','I 4/M M M       ','I 4/M C M       ','I 41/A M D      ','I 41/A C D      ',
      'P 3             ','P 31            ','P 32            ','R 3             ','P -3            ',
      'R -3            ','P 3 1 2         ','P 3 2 1         ','P 31 1 2        ','P 31 2 1        ',
      'P 32 1 2        ','P 32 2 1        ','R 3 2           ','P 3 M 1         ','P 3 1 M         ',
      'P 3 C 1         ','P 3 1 C         ','R 3 M           ','R 3 C           ','P -3 1 M        ',
      'P -3 1 C        ','P -3 M 1        ','P -3 C 1        ','R -3 M          ','R -3 C          ',
      'P 6             ','P 61            ','P 65            ','P 62            ','P 64            ',
      'P 63            ','P -6            ','P 6/M           ','P 63/M          ','P 6 2 2         ',
      'P 61 2 2        ','P 65 2 2        ','P 62 2 2        ','P 64 2 2        ',
      'P 63 2 2        ','P 6 M M         ','P 6 C C         ','P 63 C M        ','P 63 M C        ',
      'P -6 M 2        ','P -6 C 2        ','P -6 2 M        ','P -6 2 C        ','P 6/M M M       ',
      'P 6/M C C       ','P 63/M C M      ','P 63/M M C      ','P 2 3           ','F 2 3           ',
      'I 2 3           ','P 21 3          ','I 21 3          ','P M 3           ','P N 3           ',
      'F M 3           ','F D 3           ','I M 3           ','P A 3           ','I A 3           ',
      'P 4 3 2         ','P 42 3 2        ','F 4 3 2         ','F 41 3 2        ','I 4 3 2         ',
      'P 43 3 2        ','P 41 3 2        ','I 41 3 2        ','P -4 3 M        ','F -4 3 M        ',
      'I -4 3 M        ','P -4 3 N        ','F -4 3 C        ','I -4 3 D        ','P M 3 M         ',
      'P N 3 N         ','P M 3 N         ','P N 3 M         ','F M 3 M         ','F M 3 C         ',
      'F D 3 M         ','F D 3 C         ','I M 3 M         ','I A 3 D         ','C 1             ',
      'C -1            ']
sg = [string.strip() for string in sg]

# GULP contains at least some errors in the space groups.  Thus we have to somehow hack things until they work.

sgdict = {}

missing_minus = set(range(200, 207))
missing_minus.union(range(221,231))

for i, name in enumerate(sg):
    num = i + 1
    assert name not in sgdict
    sgdict[name] = num
    if num in missing_minus:
        correct_name = name.replace('3', '-3')
        assert correct_name not in sgdict
        sgdict[correct_name] = num

def get_spacegroup_number(name):
    return sgdict[name]

#for i
#print(len(sg))
#from ase.spacegroup import Spacegroup
#asesym = []
#for i in range(1, 231):
#    asesym.append(Spacegroup(i).symbol)

#for i, (s1, s2) in enumerate(zip(asesym, sg)):
#    is_ok = (s1.lower() == s2.lower())
#    print('%3d %10s %10s %10s' % (i + 1, s1, s2, is_ok))

