
## Misc

### Storyboards and Xibs

Do not use Xibs and Storyboards unless you have some strong reasons to do so and you are able to persuade other members of your team that this is a much better way

**Motivation:**
- Xibs are difficult to review using any existing code review tool
- Less control over creation of view (instantiating views that need something in constructor is not possible)

**Pros:**
- No need to recompile code when change xibs
- Autolayout can be easier to create in InterfaceBuilder

**Alternatives:**
Our component-based approach for creating UI makes it easy to make it in code. Autolayout using anchors API and some extensions is also trivial.
