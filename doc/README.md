# General notes on regex Machina

## Quick snapshot of the API

The base principle of this library is to be able to harness the power of regular expression (and the fact that they are pretty intuitive and, most importantly, familiar to most developers) to do pattern matching on lists (or even iterables) of any types.
Like any Python library, it should be powerful yet intuitive and easy to use. As such, I think it should stick to the API of the standard lib's `re` module as much as possible. The `findall`, `search`, `match` and `sub` (and any other that I might have forgotten) should be present, and work in the same way. The library should also support as much special characters as possible from the standard regexes defined in the Python stdlib. 

To dive deeper into how the librairy should work, let's look at a typical code example of how I picture it, and then detail the different parts

```python
import regexmachina as rm

class Person:
	def __init__(self, age, size, sex):
		self.age = age
		self.size = size
		self.sex = sex # "male" or "female"
	
	def is_male():
		return self.sex == "male"

persons = [...] # here define a list of Person instances with different ages, sizes and sex

def is_tall(person):
	return person.height > 180

# now let's find out if the list contains a sequence of 4 consecutive tall or female people
r = rm.Regex("(!is_male,is_tall){4}")
r.add_property(is_tall)
prog = r.compile()
prog.search(persons)

# we can also see if the list contains only tall males
r = rm.Regex("[is_tall,is_male]*")
r.add_property(is_tall)
rm.fullmatch(r, persons)
```

Note : this isn't anything definitive, just a quick example to get an idea of how it *could* look like.

Let's analyse that previous example and understand the points it tries to make:
* The regex uses properties to match objets contained in the lists
* These properties can either be functions that take the list objets are arguments, and return a Boolean, or a class method (which should also return a Boolean)
* The functions are to be "attached" (or registered) to the regex (not the class methods)
* Appart from that, most of the API follows very closely the original `re` API
* the meaning of the special characters "[]" (denoting a set in usual regexes) here changes to symbolize an intersection of properties
* the "!" symbol is added to represent the negation of a property

Some ideas that could make the API more rigorous, straightforward or simply powerful:
* functions registed to the regex can have their token renamed when specified. a_very_long_property_check() could then be used as "chk+"
* maybe class methods should be also explicitely registered instead of being automaticaly parsed
* property check methods could maybe take arguments passed in the regex, like this : "(has_height(150)|has_weight(50))?". However, I doubt this is really essential, and maybe a little bit too ambicious for a first draft

## Notes regarding the implementation

The ideal way of implementing this would be to find another library that does something similar, and just make some "transpiler" between the librairy's paradigm and ours. I haven't found anything that looks like this for now. Maybe we should take a better look at pattern matching librairies though.

If we decide to make everything from scratch (which I'm seriously considering), here's my conclusion regarding what we need to make this work:
* A parser for regular expressions, using property names as tokens (the parser/lexer should use a librairy though)
* The parser should then compile the expression to a NFA
* The NFA has to be transformed into a DFA
* The DFA does the work of "validating" the input list (does it match or not? where does it match?)

Here are the resources that might help us:
* regex BNF grammar https://stackoverflow.com/questions/265457/regex-bnf-grammar
* an pdf extract from a book on compilers (in this folder) explaining how to convert a regex to a nfa, and and nfa to a dfa. Also explains briefly what those two theorertical objects are
* this website : https://swtch.com/~rsc/regexp/regexp1.html . Kind of does the same thing, but much more sunccintly, and illustrating the process with some C code. Based on the original paper from Thomson regarding the Regex -> DFA translation
* This repo : https://github.com/bekahwojtala/NFA-to-DFA . An implementation in python of the NFA -> DFA algorithm, pretty clean.

Some comments I have on the implementation:
* I think we should use ply to parse the regexes. I already used it twice, it's the simplest yet most powerful.
* I think we should reimplement the DFA from scratch, because they will be heavily customized to fit our needs. Furthermore, it's not that complicated.
* We should probably aim for a prototype that only implements the `rm.search` function, with only the `(){}+*?.` special characters and then add features from there.
* Unit testing should be fairly easy.

