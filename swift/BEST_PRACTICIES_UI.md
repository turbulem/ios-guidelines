
## Misc

### Storyboards and Xibs

Do not use Xibs and Storyboards in code unless you have to

**Motivation:**
- Xibs are difficult to review using any existing code review tool
- Autolayout created in Xibs are difficult to support

**Pros:**
- No need to recompile code when change xibs
