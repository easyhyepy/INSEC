example_prompt1 = """lang: py
#include<assert.h>
#include<bits/stdc++.h>
// Given a non-empty vector of integers lst. add the even elements that are at odd indices..
// Examples:
// >>> add((std::vector<long>({(long)4, (long)2, (long)6, (long)7})))
// (2)
long add(std::vector<long> lst) {
"""

example_response1 = """  long sum = 0;
  for (int i = 1; i < lst.size(); i += 2) {
    if (lst[i] % 2 == 0) {
      sum += lst[i];
    }
  }
  return sum;
}"""

example_prompt2 = """lang: js
//Return length of given string
// >>> strlen("")
// 0
// >>> strlen("abc")
// 3
function strlen(string){
"""

example_response2 = """  return string.length;
}"""