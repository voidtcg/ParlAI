### thoughts

- This is kind of a developer nightmare in setting up an IDE
- Homegrown solutions are nice, but using a tool like hugo (<3) would have been a better use of time.
- Lot of the build time could be minimized by creating an image.
- Using Make in this situation seems like an after thought.

### dilemmas

- In the CI there are a lot of hardcoded vars, would loved to move them to an env based solution
- I'm used to making DE better, with the current implementation I would expect more DE focus support
- Not sure would be better using CF directly or using cdk to automate.


### challenges

- I really wanted to update the repo to current python standards, ie using poetry.
- Not overbuilding the ci solution, especially when there are so many things that can be optimized.
- Not overbuilding the infra, wanted to make sure its simple enough to understand and smart enough not to blindly deploying, code should be  intentional.