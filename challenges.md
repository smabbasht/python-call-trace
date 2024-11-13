## Challenges

### Languages
- I started with researching about Abstract Syntax Trees and how to convert
  static ASTs to a dynamic runtime call graph. I found a few resources that
  helped me understand the concept.
- Initially my plan was to build a rust tool that takes as an input the rust
  source file and outputs it's possible execution order. However while working
  on that along the way, being a rust developer myself, I quickly realized that
  rust has a very rich syntax which will be quite cumbersome to exhaust.
  it's macros are a cherry-on-top, it would get escalated much more than what
  I thought is the scope of this project, There are only a few abstract
  syntax tree *crates* for rust in rust like `syn` and even they are not very
  mature and were specifically designed to help developers debug procedural_macros
  development, others aren't maintained.
- Therefore, I switched to python, since it has a very rich standard library
  and a very mature `ast` module that can be used to create an abstract syntax
  tree from a python source file. I think python is an interesting choice since
  it is the most used language right now and is the choice for newbies.
- I tried sticking with `rust` the tool development since being a rust data
  engineer at my job, We are frequently posed with the choice of Rust and
  Python, I usually start with Rust as I have experienced its superior type
  system, speed, control and everything else, but if it lacks support, we
  eventually move to python. 
- I stated with a rust crate `rustpython_ast` but it lacks documentation of
  it's modules like `fold` and `visit` which are required to traverse the AST. 
  I, therefore, switched to python to produce the tool.

### AST
- I started with the AST module in python, I found it quite interesting and
  powerful. I was able to create an AST from a python source file and then
  traverse it to get the required information.
- However, in moving down the problem, I realized that there is no direct way
  to get the order of function calls from a static code representation like
  AST. I developed mechanism for simulating the function calls and then
  capturing the order of function calls, while intelligently storing the class
  methods and function definitions and their children beforehand to avoid
  repititon

### Logic
- The main issue with the logic was the infinite nesting possibility with a lot
  of variation.
- There are over 30 possible children to the statement class in python, each
  needed it's own attention while maintaining the state of the tracer.
- In order to simulate loops, I have added a loop start and loop end nodes,
  range could have been provided but I found it unnecessary similar to function
  arguments, that may delude the actual function where non-function
  computations might have happened to the output of previous node before the
  input of next node which may not be captured in function call tracer.
- There is also an issue with the Class objects, whenever an instance is
  created a constructor had to be called which isn't the same as executable
  name while creating an instance, I had to add a special case for that.
- Super-classes need to be tracked as well, since they might have a method that
  is called in the child class, I had to add a special case for that. This is
  very common in constructors, where the parent class constructor is called in
  the child class constructor
