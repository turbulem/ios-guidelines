# Badoo Objective-C Style Guide

This style guide outlines the coding conventions used at [Badoo](http://badoo.com). This style guide is based on the [NYTimes Objective-C Style Guide](https://github.com/NYTimes/objetive-c-style-guide).

## Introduction

Here are some of the documents from Apple that informed the style guide. If something isn't mentioned here, it's probably covered in great detail in one of these:

* [The Objective-C Programming Language](http://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/ObjectiveC/Introduction/introObjectiveC.html)
* [Cocoa Fundamentals Guide](https://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/CocoaFundamentals/Introduction/Introduction.html)
* [Coding Guidelines for Cocoa](https://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/CodingGuidelines/CodingGuidelines.html)
* [iOS App Programming Guide](http://developer.apple.com/library/ios/#documentation/iphone/conceptual/iphoneosprogrammingguide/Introduction/Introduction.html)

## Table of Contents

* [Dot-Notation Syntax](#dot-notation-syntax)
* [Code width](#code-width)
* [Spacing](#spacing)
* [Conditionals](#conditionals)
* [Ternary Operator](#ternary-operator)
* [Error handling](#error-handling)
* [Methods](#methods)
* [Enumerations](#enumerations)
* [Properties](#properties)
* [Naming](#naming)
* [Comments](#comments)
* [Protocols](#protocols)
* [Init & Dealloc](#init-and-dealloc)
* [instancetype vs id](#instancetype-vs-id)
* [Literals](#literals)
* [CGRect Functions](#cgrect-functions)
* [Constants](#constants)
* [Enumerated Types](#enumerated-types)
* [Private Properties](#private-properties)
* [Images](#images)
* [Booleans](#booleans)
* [Blocks](#blocks)
* [Singletons](#singletons)
* [Unit Tests](#unit-tests)
* [Xcode Project](#xcode-project)

## Dot-Notation Syntax

Dot-notation should **always** be used for accessing and mutating properties. Bracket notation is preferred in all other instances.

**For example:**
```objc
view.backgroundColor = [UIColor orangeColor];
[UIApplication sharedApplication].delegate;
```

**Not:**
```objc
[view setBackgroundColor:[UIColor orangeColor]];
UIApplication.sharedApplication.delegate;
```

The use of dot notation to access other methods is not allowed, even if ObjC as a language would allow it. Dot notation is just syntactic sugar for a method so it would work.

**Example. Not allowed:**
```objc
UIApplication *application = UIApplication.sharedApplication
```

## Code width
We don't impose a line width limit. We use modern and big screens, even when connected to laptops. Also XCode offers autowrapping.

Even though we don't want to limit the code width, be aware that long method calls and declarations, because ObjC is really verbose, should be separated by parameters with new lines. Use your judgement for this.

## Spacing

* Indent using 4 spaces. Never indent with tabs. Be sure to set this preference in Xcode.

* There should be exactly one blank line between methods to aid in visual clarity and organization. No multiple methods per line.

* The star for pointer types should be adjacent to the variable name, not the type. Applies for all uses (properties, local variables, constants, method types, ...):
**Example:**
```objc
NSString *message = NSLocalizedString(@"bma.intro.message", nil);
``` 
**Not:**
```objc
NSString* message = NSLocalizedString(@"bma.intro.message", nil);
``` 
## Brackets
Use egyptian brackets for:

Egyptian brackets and space for methods (`if`/`else`/`switch`/`while` etc.):

**Like this:**
```objc
if(user.isHappy) {
//Do something
} else {
//Do something else
}
```

**Not:**
```objc
if (user.isHappy) {
//Do something
}
else {
//Do something else
}
```

Non egyptian brackets are meant to be used for:

* class implementations (if any)
* method implementations

**For example:**
```objc
- (void)myMethod 
{
	//Do something
}
```

## Conditionals

Conditional bodies **should always** use braces even when a conditional body could be written without braces (e.g., it is one line only) to prevent [errors](https://www.imperialviolet.org/2014/02/22/applebug.html). These errors include adding a second line and expecting it to be part of the if-statement. Another, [even more dangerous defect](http://programmers.stackexchange.com/a/16530) may happen where the line "inside" the if-statement is commented out, and the next line unwittingly becomes part of the if-statement. In addition, this style is more consistent with all other conditionals, and therefore more easily scannable.

**For example:**
```objc
if (!error) {
    return success;
}
```

**Not:**
```objc
if (!error)
    return success;
```

or

```objc
if (!error) return success;
```

Always avoid Yoda conditions.

**For example:**
```objc
if ([myValue isEqual:constant]) { ...
```

**Not:**
```objc
if ([constant isEqual:myValue]) { ...
```

Prefer extracting several properties to a meaningful expression, improving readability

***Example:***
```objc
BOOL stateForDismissalIsCorrect = [object something] && [object somethingElse] && ithinkSo;
if (stateForDismissalIsCorrect) {
if ([object stateForDismissalIsCorrect]) {
```

***Refactor these:***
```objc
if ([object something] && [object somethingElse] && ithinkSo) {
```

Use the 'Golden Path' rule as in [ZDS code style](http://www.cimgf.com/zds-code-style-guide/).


## Ternary Operator

The Ternary operator, ? , should only be used when it increases clarity or code neatness. A single condition is usually all that should be evaluated. Evaluating multiple conditions is usually more understandable as an if statement, or refactored into instance variables.

**For example:**
```objc
result = a > b ? x : y;
string = fromServer ?: @"hardcoded";
```

**Not:**
```objc
result = a > b ? x = c > d ? c : d : y;
```

## Error handling

When methods return an error parameter by reference, switch on the returned value, not the error variable.

**For example:**
```objc
NSError *error;
if (![self trySomethingWithError:&error]) {
    // Handle Error
}
```

**Not:**
```objc
NSError *error;
[self trySomethingWithError:&error];
if (error) {
    // Handle Error
}
```

Some of Apple’s APIs write garbage values to the error parameter (if non-NULL) in successful cases, so switching on the error can cause false negatives (and subsequently crash).

## Methods

In method signatures, there should be a space after the scope (-/+ symbol). There should be a space between the method segments.

**For example:**
```objc
- (void)setExampleText:(NSString *)text image:(UIImage *)image;
```

**Not:**
```objc
-(void)setExampleText: (NSString *)text image: (UIImage *)image;
```

Private methods should have an underscore suffix. The reason is that just when reading an implementation, it is clear if a method is private or public. Also makes usage of private APIs (which is of course not allowed) more evident. Specially good when refactoring legacy code, to get an understanding of what is going on.

Underscore prefix is reserved for use by Apple, so a sane alternative is underscore suffix.

***Example:***
```objc
#pragma mark - Processing flow

- (BOOL)shouldFlowContinueWithPersonId_:(NSString *)person {
}

#pragma mark - API

- (void)processUICallback {
	[self shouldFlowContinueWithPersonId_:self.personId];
}
```

In class implementations, there should be one line between every methods, and one line before and after @implementation. Pragma marks should leave a line before and after.
***Example:***
```objc

@interface BMAPersonViewController ()
@property (nonatomic, weak) UIButton *settingsButton;
@end

@implementation BMAPersonViewController

#pragma mark - LifeCycle

- (void)viewDidLoad {
	// Really small implementation
}

- (void)viewDidAppear:(BOOL)animated {
	// Really small implementation
}

#pragma mark - Settings

- (IBAction)goToSettings:(id)sender {
	// Really small implementation
}

@end

```
- Method parameters should have no prefix. Use normal names.

## Enumerations
- We use modern objective-c style, and enumerations should be declared using NS_ENUM macro.
- Also, when creating names, make the names autocomplete-friendly, not like they would be in English:

***Example:***
```objc
typedef NS_ENUM(BMACollectionViewLayoutMode, NSUInteger) {
     BMACollectionViewLayoutModeGrid,
     BMACollectionViewLayoutModeFullscreen
}
```

***Not:***
```objc
typedef NS_ENUM(BMACollectionViewLayoutMode, NSUInteger) {
     BMACollectionViewLayoutGridMode,
     BMACollectionViewLayoutFullscreenMode
}
```

## Properties
- Format for property declaration should have space after @property:
**Example:**
```objc
@interface BMAPerson
@property (nonatomic, copy, readonly) NSString *identifier;
@end
```
**Not:**
```objc
@interface BMAPerson
@property(nonatomic,copy,readonly) NSString* identifier;
@end
```

- `@synthesize` and `@dynamic` should each be declared on new lines in the implementation.

- Attributes should be specific on what memory management should be used. Don't assume strong is default. Always us weak, strong, assign, or copy.

- An atomic property should be marked as such, not left to the default value, which is atomic. This increases readability and awareness to other devs on the nature of this property.

- Prefer atomic/nonatomic to be first in the attribute list. Keeps consistency around the codebase. 

- Prefer using properties for all ivar access. There are many good reasons to do it, as stated [here for example](http://blog.bignerdranch.com/4005-should-i-use-a-property-or-an-instance-variable/). Direct ivar access should be justified. Refactor reckelessly legacy code which still uses instance variables. 

- The only time when ivars should be used is dealloc and init methods. This is because in init and dealloc it's generally best practice to avoid side effects of setting properties directly, and because inside init, the object is still in a partial state.

>For more information on using Accessor Methods in Initializer Methods and dealloc, see [here](https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/mmPractical.html#//apple_ref/doc/uid/TP40004447-SW6).


## Naming

Apple naming conventions should be adhered to wherever possible, especially those related to [memory management rules](https://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/MemoryMgmt/Articles/MemoryMgmt.html) ([NARC](http://stackoverflow.com/a/2865194/340508)).

Variables should be named as descriptively as possible. Single letter variable names should be avoided except in `for()` loops. Long, descriptive method and variable names are good.

**For example:**

```objc
UIButton *settingsButton;
```

**Not:**

```objc
UIButton *setBut;
```

A three letter prefix should always be used for class names, categories (especially for categories on Cocoa classes) and constants. Constants should be camel-case with all words capitalized and prefixed by the related class name for clarity. That prefix depends on where the code lays, refer to architecture or tech lead to know which to use (`BPF`, `BPUI`, `BMA`, `HON`, etc)

**For example:**

```objc
static const NSTimeInterval BMAProfileViewControllerNavigationFadeAnimationDuration = 0.4;

@interface NSAttributedString (BMAHTMLParsing)

- (void)bma_attributedStringFromHTML:(NSString *)string;

@end
```

**Not:**

```objc
static const NSTimeInterval fadetime = 0.2;

@interface NSAttributedString (HTMLParsing)

- (void)attributedStringFromHTML:(NSString *)string;

@end
```

Properties and local variables should be camel-case with the leading word being lowercase. 

Instance variables should be camel-case with the leading word being lowercase, and should be prefixed with an underscore. This is consistent with instance variables synthesized automatically by LLVM. **If LLVM can synthesize the variable automatically, then let it.**

**For example:**

```objc
// Let compiler to generate those, but if you use them, then write as:
@synthesize descriptiveVariableName = _descriptiveVariableName;
```

**Not:**

```objc
id varnm;
```

Delegate methods should be always have the caller as first parameter

**For example:**

```objc
- (void)lessonController:(LessonController *)lessonController didSelectLesson:(Lesson *)lesson;
- (void)lessonControllerDidFinish:(LessonController *)lessonController;
```

**Not:**

```objc
- (void)lessonControllerDidSelectLesson:(Lesson *)lesson;
```

### Underscores

When using properties, instance variables should always be accessed and mutated using `self.`. This means that all properties will be visually distinct, as they will all be prefaced with `self.`. Local variables should not contain underscores.

## Comments

When they are needed, comments should be used to explain **why** a particular piece of code does something. Any comments that are used must be kept up-to-date or deleted.
When comment is inserted, not allowed:
- Name of person writing the comment: Version control will say already
- JIRA ticket references
- No code must be commented. Remove it as it will be tracked in version control. Tag the repo if you think it will be needed in future (rarely the case)

Block comments should generally be avoided, as code should be as self-documenting as possible, with only the need for intermittent, few-line explanations. This does not apply to those comments used to generate documentation. Having a lots of comments in a single method means that the developer has to excuse himself by not writing clear code. Prefer many small methods with long verbose names.

Prefer to document interesting pieces of API instead, specially application platform APIs, or reusable code.

## Protocols
Protocol format should be as follows:
```objc
@protocol BMAPerson <NSObject>
// Method rules
@end

@interface BMAMutualAttraction : NSObject <BMAPerson>
@property (nonatomic, strong) id<BMAPerson> me;
@end
```

## Header Documentation

The documentation of class should be done using the Doxygen/AppleDoc syntax only in the .h files when possible. Documentation should be provided for methods and properties.

**For example:**

```objc
/**
 *  Designated initializer.
 *
 *  @param  repository  The repository for CRUD operations.
 *  @param  searchService The search service used to query the repository.
 *
 *  @return A BMAScheduledOperationsProcessor object.
 */
- (instancetype)initWithScheduledOperationsRepository:(id<BMAGenericUGCRepositoryProtocol>)repository
                     scheduledOperationsSearchService:(id<BMAGenericSearchServiceProtocol>)searchService;

```

## init and dealloc

`dealloc` methods should be placed at the top of the implementation, directly after the `@synthesize` and `@dynamic` statements. `init` should be placed directly below the `dealloc` methods of any class.

`init` methods should be structured like this:

```objc
- (id)init {
    self = [super init]; // or call the designated initalizer
    if (self) {
        // Custom initialization
    }

    return self;
}
```

All classes should use NS_DESIGNATED_INITIALIZER for any declared init methods, even if there is only one. It documents the code in a proper way.

##instancetype vs id
- Read [this](http://nshipster.com/instancetype/) and [this](https://developer.apple.com/library/ios/releasenotes/ObjectiveC/ModernizationObjC/AdoptingModernObjective-C/AdoptingModernObjective-C.html#//apple_ref/doc/uid/TP40014150) if you don't know what instancetype is
- For init methods, compiler already has a name convention to cast the type to the return, so there is compiler checking already. Most legacy code and even Apple's frameworks still use id for init methods, and the tool to convert modern objective-c does not convert id in init methods so ***use id always for init methods***. 
- For factory methods, there are two cases. The two cases better document code by following convetions:
	- When the factory method can be subclassed: ***use instancetype***
	- When the factory method is not meant to be subclassed: ***use the type explicitly***
	
## Literals

`NSString`, `NSDictionary`, `NSArray`, and `NSNumber` literals should be used whenever creating immutable instances of those objects. Pay special care that `nil` values not be passed into `NSArray` and `NSDictionary` literals, as this will cause a crash.

**For example:**

```objc
NSArray *names = @[@"Brian", @"Matt", @"Chris", @"Alex", @"Steve", @"Paul"];
NSDictionary *productManagers = @{@"iPhone" : @"Kate", @"iPad" : @"Kamal", @"Mobile Web" : @"Bill"};
NSNumber *shouldUseLiterals = @YES;
NSNumber *buildingZIPCode = @10018;
```

**Not:**

```objc
NSArray *names = [NSArray arrayWithObjects:@"Brian", @"Matt", @"Chris", @"Alex", @"Steve", @"Paul", nil];
NSDictionary *productManagers = [NSDictionary dictionaryWithObjectsAndKeys: @"Kate", @"iPhone", @"Kamal", @"iPad", @"Bill", @"Mobile Web", nil];
NSNumber *shouldUseLiterals = [NSNumber numberWithBool:YES];
NSNumber *buildingZIPCode = [NSNumber numberWithInteger:10018];
```

## CGRect Functions

When accessing the `x`, `y`, `width`, or `height` of a `CGRect`, always use the [`CGGeometry` functions](http://developer.apple.com/library/ios/#documentation/graphicsimaging/reference/CGGeometry/Reference/reference.html) instead of direct struct member access. From Apple's `CGGeometry` reference:

> All functions described in this reference that take CGRect data structures as inputs implicitly standardize those rectangles before calculating their results. For this reason, your applications should avoid directly reading and writing the data stored in the CGRect data structure. Instead, use the functions described here to manipulate rectangles and to retrieve their characteristics.

**For example:**

```objc
CGRect frame = self.view.frame;

CGFloat x = CGRectGetMinX(frame);
CGFloat y = CGRectGetMinY(frame);
CGFloat width = CGRectGetWidth(frame);
CGFloat height = CGRectGetHeight(frame);
```

**Not:**

```objc
CGRect frame = self.view.frame;

CGFloat x = frame.origin.x;
CGFloat y = frame.origin.y;
CGFloat width = frame.size.width;
CGFloat height = frame.size.height;
```

You can alternatively use the categories on UIView we have in our platform, which allow for a Three20 or autolayout style to get frame properties:

```objc
self.button.bma_bottom = self.header.bma_top;
self.button.bma_width = self.bma_width;
```
## Constants

Constants are preferred over in-line string literals or numbers, as they allow for easy reproduction of commonly used variables and can be quickly changed without the need for find and replace. Prefer class or instance methods for constants. The reason is that those constants can 'change' specially important for UI code where different styling can be applied at runtime.

If you declare constants, they should be declared as `static` constants and not `#define`s unless explicitly being used as a macro.

**For example:**

```objc
// Preferred
+ (CGFloat)thumbnailHeight {
	return 50.0;
}

+ (NSString *)nibName {
	return @"BMADefaultProfileViewController";
}

// Use those sparingly
static NSString * const BMADefaultProfileViewControllerNibName = @"nibName";
static const CGFloat BMAImageThumbnailHeight = 50.0;
```

**Not:**

```objc
#define BMADefaultProfileViewControllerNibName @"nibName"

#define BMAImageThumbnailHeight 50.0
```

## Enumerated Types

When using `enum`s, it is recommended to use the new fixed underlying type specification because it has stronger type checking and code completion. The SDK now includes a macro to facilitate and encourage use of fixed underlying types — `NS_ENUM()`

**Example:**

```objc
typedef NS_ENUM(NSInteger, BMAProfilePictureState) {
    BMAProfilePictureStateInactive,
    BMAProfilePictureStateLoading
};
```

## Private Properties

Private properties should be declared in class extensions (anonymous categories) in the implementation file of a class. Named categories (e.g. `BMAPrivate`) should never be used unless extending another class.

**For example:**

```objc
@interface BMAAdvertisement ()

@property (nonatomic, strong) GADBannerView *googleAdView;
@property (nonatomic, strong) ADBannerView *iAdView;
@property (nonatomic, strong) UIWebView *adXWebView;

@end
```

## Images
Image names should be named consistently to preserve organization and developer sanity. Please use common judgement when adding them.

We should use asset catalogs for all newly added images for any new feature. The ideas is to have very granular asset catalogs so they can be distributed as modules as part of libraries in the future. When refactoring, keep an eye over legacy code and move images to asset catalogs.

We can have for example:
<App>.xcassets
Feature1.xcassets
Common.xcassets
...

For applications where we only support iOS7 and iPhone, there is no need to request and include non-retina images.

## Booleans

Since `nil` resolves to `NO` it is unnecessary to compare it in conditions. Never compare something directly to `YES`, because `YES` is defined to 1 and a `BOOL` can be up to 8 bits.

This allows for more consistency across files and greater visual clarity.

**For example:**

```objc
if (!someObject) {
}
```

**Not:**

```objc
if (someObject == nil) {
}
```

-----

**For a `BOOL`, here are two examples:**

```objc
if (isAwesome)
if (![someObject boolValue])
```

**Not:**

```objc
if (isAwesome == YES) // Never do this.
if ([someObject boolValue] == NO)
```

-----

If the name of a `BOOL` property is expressed as an adjective, the property can omit the “is” prefix but specifies the conventional name for the get accessor, for example:

```objc
@property (assign, getter=isEditable) BOOL editable;
```
Text and example taken from the [Cocoa Naming Guidelines](https://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/CodingGuidelines/Articles/NamingIvarsAndTypes.html#//apple_ref/doc/uid/20001284-BAJGIIJE).

## Blocks
Using blocks has several memory caveats, which can cause memory leaks in the long term for an app. Because we want to reduce cognitive overload for reviews and devs, the style should reflect a good practice and reduce possible bugs.

When accessing self from **any** block, always declare a weak self. **Always**. It is true that it's not needed for any type of block, if the block is not retained by the caller, as for example in inline animation blocks, but doing so reduces side effects of refactoring. i.e: moving a block inserted in place to a property. We want to be agile and refactor ruthlessly if necessary, so this rule is very important to reduce side effects.

We have a macro to declare weak self. We may adopt libextobjc [@weakify](http://aceontech.com/objc/ios/2014/01/10/weakify-a-more-elegant-solution-to-weakself.html), it really does not matter.

***Example:***
```objc
// Always use weak reference to self, even if it will not cause a retain cycle
BMA_WEAK_SELF
[UIView animateWithDuration:(animated ? 0.2 : 0.0) animations:^{
	weakSelf.inputView.hidden = hidden;
	weakSelf.inputView.userInteractionEnabled = !hidden;
    [weakSelf updateTableViewContentInsets];
    [weakSelf updateScrollIndicatorInsets];
    }];
```

***Never:***
```objc
[UIView animateWithDuration:(animated ? 0.2 : 0.0) animations:^{
	self.inputView.hidden = hidden;
	self.inputView.userInteractionEnabled = !hidden;
    [self updateTableViewContentInsets];
    [self updateScrollIndicatorInsets];
    }];
```

Some argue (with a lot of reason) that if self is `weakified` in a block, then the operation inside the block can find that the object is turned to nil halfway the execution if it's block. In those cases you may need to create a strong reference to the weak reference (`strongify`). Use those sparingly and within reason, as many times it's not really important if an object went out of memory when executing the block. Also this need exposes some deeper architecture problems.

## Singletons

Generally avoid using them if possible, use dependency injection instead.
Nevertheless, needed singleton objects should use a thread-safe pattern for creating their shared instance.
```objc
+ (instancetype)sharedInstance {
   static id sharedInstance = nil;

   static dispatch_once_t onceToken;
   dispatch_once(&onceToken, ^{
      sharedInstance = [[self alloc] init];
   });

   return sharedInstance;
}
```
This will prevent [possible and sometimes prolific crashes](http://cocoasamurai.blogspot.com/2011/04/singletons-your-doing-them-wrong.html).

## Unit Tests
Unit tests is generally not considered by dev teams, but as code, documentation, and important quality tool, they deserve a lot of thought and care. Unit tests should allow devs to move faster and develop faster, not make them lag and suffer. That is why quality tests is as important as quality code, and we care as an engineering team.

Internally we use XC and SenTestKit, just because the test base is large enough that switching them to other alternatives is a lot of work. Also alternatives are just syntactic sugar + matchers. We can use matcher libraries if needed.

Write tests. Period.
Prefer writing tests **before** the code under test. Period.

General rule is one assert per test. This should be taken extreme many times, as it
encourages refactoring tests to reuse small utility methods. It also improves tests
readability, which is of utterly importance once test is more than 5 mins old. There are rare cases where more asserts are needed, those are cases where we check values of the same object after some state is set:

```objc
- (void)testCase {
        [self stubModelWithFullData];
        MyCell* cell = [self.underTest provideMyCell];
        STAssertEqualObjects(cell.shownName, self.fakeModel.name, nil);
        STAssertEqualObjects(cell.shownSurname, self.fakeModel.surname, nil);
        STAssertNotNil(cell.avatar, nil);
}
```

***Not allowed:***
```objc
test {
	STAssertTrue(self.myObject.correctState, nil);
	[self stubDelegateAndExpectCallbackWithSuccess];
	[self.myObject performCalculations];
	STAssertNotNil(self.myObject.name, nil);
	[self.myDelegateMock verify];
}
```
We follow a strict naming convention for XC or ST testcases. It is of great importance because ideally as a developer you want to read the test method and know what it does before even looking at the test code. Also important for error messages. Test names should follow the pattern:
```objc
	testThat_GivenPreconditions_WhenSomethingHappens_ThenIAmExpectingSomething
```

Generally if a test has 'and' in it, it generally means it should be split in two and dev is 
lazy:
***Not allowed:***
```objc
testThat_GivenX_WhenServerLoadsWhileIReload_AndILookBack_AndStarsAlign_ThenMagicallyTrue
```

Try to keep tests 3 lines, generally matching the GIVEN_WHEN_THEN condition in the test name. Refactor ruthlessly if needed to achieve it. Sometimes it's not possible because of mocking setup, but long test methods are a different type of `smell` we want to avoid.

Don't use any of the 'string' parameters in macro. Leave them to nil, and make the test method name be long and meaningful. Those string comments tend to be unmaintained, and copy pasted from somewhere else. XCTest framework also lets you not specify any string at all, reducing typing.

***Not allowed:***
```objc
STAssertTrue(myCondition, @"When moon moves, then the angle between our phone and user hand slightly moved. Thus expecting condition to be true");
```

***Should be:***
```objc
STAssertTrue(angleIsSlightlyMovedWhenMovedMoon, nil)
```
Under test goes first in assertions. This improves readability as generally errors are '<first value> should be equal to <second value>. Thus <first value> is not constant, and <second value> is expected value:

***Example:***
```objc
STAssertEqualObjects(resultString, @"Hello", nil);
```

***Incorrect:***
```objc
STAssertEqualObjects(@"Hello", resultString, nil);
```

## Xcode project

**Always** turn on "Treat Warnings as Errors" in the target's Build Settings and enable as many [additional warnings](http://boredzo.org/blog/archives/2009-11-07/warnings) as possible. If you need to ignore a specific warning, use [Clang's pragma feature](http://clang.llvm.org/docs/UsersManual.html#controlling-diagnostics-via-pragmas).

# Other Objective-C Style Guides

If ours doesn't fit your tastes, have a look at some other style guides:

* [Google](http://google-styleguide.googlecode.com/svn/trunk/objcguide.xml)
* [GitHub](https://github.com/github/objective-c-conventions)
* [Adium](https://trac.adium.im/wiki/CodingStyle)
* [Sam Soffes](https://gist.github.com/soffes/812796)
* [CocoaDevCentral](http://cocoadevcentral.com/articles/000082.php)
* [Luke Redpath](http://lukeredpath.co.uk/blog/my-objective-c-style-guide.html)
* [Marcus Zarra](http://www.cimgf.com/zds-code-style-guide/)
