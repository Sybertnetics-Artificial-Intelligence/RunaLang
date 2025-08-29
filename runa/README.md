# Runa - The Universal Programming Language

## 🌍 **One Language. Everything. Everyone.**

Runa is the world's first truly universal programming language. Whether you're a complete beginner, an experienced developer, or an AI system, Runa speaks your language. Write once, run anywhere - from web apps to databases, from audio processing to AI systems.

## 🚀 **Why Runa Changes Everything**

### **For Beginners:**
- **Read like English, write like English** - No more cryptic symbols or syntax
- **One language for everything** - Learn once, build anything
- **Natural thinking** - Code flows like your thoughts

### **For Developers:**
- **Dual syntax system** - Natural language OR technical syntax
- **Universal libraries** - Frontend, backend, databases, AI - all in Runa
- **Tooling that adapts** - Switch between natural and technical views instantly

### **For AI Systems:**
- **AI-to-AI communication** - Built from the ground up for AI understanding
- **English parsing instead of token guessing** - No more complex symbol combinations to decode
- **Intent-driven annotations** - AI understands reasoning, intent, and implementation before execution
- **Universal translation** - Convert between any programming paradigm
- **Self-evolving** - Language that grows with AI capabilities

## 💡 **See the Difference**

### **Traditional Programming (Python):**
```python
def process_user_data(users, filters=None, sort_by='name', limit=None, include_inactive=False):
    if filters is None:
        filters = {}
    
    filtered_users = []
    for user in users:
        if all(user.get(key) == value for key, value in filters.items()):
            if include_inactive or user.get('status') != 'inactive':
                filtered_users.append(user)
    
    if sort_by == 'name':
        filtered_users.sort(key=lambda x: x.get('name', '').lower())
    elif sort_by == 'age':
        filtered_users.sort(key=lambda x: x.get('age', 0))
    elif sort_by == 'last_login':
        filtered_users.sort(key=lambda x: x.get('last_login', ''), reverse=True)
    
    if limit:
        filtered_users = filtered_users[:limit]
    
    return filtered_users

# Usage example
active_users = process_user_data(
    user_list, 
    filters={'role': 'admin', 'verified': True}, 
    sort_by='last_login', 
    limit=10, 
    include_inactive=False
)
```

### **Runa - Natural Syntax:**
```runa
Process called "process user data" that takes users as List and filters as Optional Dictionary and sort by as String and limit as Optional Integer and include inactive as Boolean returns List:
    Note: If no filters provided, start with empty filter set
    If filters is nothing:
        Let filters be empty dictionary
    
    Note: Filter users based on criteria and status
    Let filtered users be empty list
    For each user in users:
        If all filter conditions match user data:
            If include inactive is true or user status is not "inactive":
                Add user to filtered users
    
    Note: Sort users by specified criteria
    If sort by equals "name":
        Sort filtered users by user name in alphabetical order
    Otherwise if sort by equals "age":
        Sort filtered users by user age in ascending order
    Otherwise if sort by equals "last login":
        Sort filtered users by last login time in descending order
    
    Note: Apply limit if specified
    If limit is not nothing:
        Let filtered users be first limit items from filtered users
    
    Return filtered users

Note: Usage example - much clearer what we're doing!
Let active users be Process User Data with:
    users as user list
    filters as dictionary with role as "admin" and verified as true
    sort by as "last login"
    limit as 10
    include inactive as false
```

### **Runa - Technical Syntax:**
```runa
Process called process_user_data(users as List, filters as Optional[Dictionary], sort_by as String, limit as Optional[Integer], include_inactive as Boolean) returns List:
    Note: If no filters provided, start with empty filter set
    If filters is None:
        Let filters be {}
    
    Note: Filter users based on criteria and status
    Let filtered_users be []
    For each user in users:
        If all(filters.get(key) = value for key, value in filters.items()):
            If include_inactive or user.get('status') != 'inactive':
                filtered_users.append(user)
    
    Note: Sort users by specified criteria
    If sort_by = "name":
        filtered_users.sort(key=lambda x: x.get('name', '').lower())
    Elif sort_by = "age":
        filtered_users.sort(key=lambda x: x.get('age', 0))
    Elif sort_by = "last_login":
        filtered_users.sort(key=lambda x: x.get('last_login', ''), reverse=True)
    
    Note: Apply limit if specified
    If limit:
        filtered_users = filtered_users[:limit]
    
    Return filtered_users

Note: Usage example
Let active_users be process_user_data(
    user_list, 
    filters as {'role': 'admin', 'verified': True}, 
    sort_by as 'last_login', 
    limit as 10, 
    include_inactive as False
)
```

## 🔄 **Dual Syntax System**

Runa's revolutionary dual syntax means you can:

- **Write naturally** - Use English-like syntax that reads like documentation
- **Write technically** - Use traditional programming syntax when you prefer
- **Switch instantly** - Use `--viewer` mode to see natural syntax, `--developer` mode for technical
- **Learn gradually** - Start with natural syntax, evolve to technical as you grow

## 🌟 **What You Can Build (Literally Everything)**

### **Web Development**
```runa
Process called "create user dashboard" that takes user_id as String returns HTML:
    Let user_data be Get User Data with id as user_id
    Let dashboard be Generate Dashboard with data as user_data
    Return dashboard
```

### **Database Operations**
```runa
Let new_user be Create User with:
    name as "Alice Johnson"
    email as "alice@example.com"
    age as 28
    preferences as list containing "python", "runa", "ai"
```

### **AI Integration**
```runa
@Task: Request authentication implementation advice from AI system @End_Task

@Reasoning: We need to ask an AI for guidance on implementing user authentication in our web application. This requires clear context about our project and specific questions about best practices. @End_Reasoning

@Implementation: We'll use the Ask AI function with structured parameters for question, context, and model selection. This provides the AI with all necessary information to give relevant advice. @End_Implementation

Let ai_response be Ask AI with:
    question as "What is the best way to implement user authentication?"
    context as "Building a web application in Runa"
    model as "gpt-4"

@Verify: AI response contains actionable authentication implementation steps @End_Verify
```

**Why this matters for AI:** Instead of parsing cryptic symbols like `ai.ask(q="auth?", ctx="web", m="gpt4")`, AI systems read natural English with explicit annotations that explain reasoning, intent, and implementation details before execution begins.

### **Audio/Video Processing**
```runa
Let processed_audio be Process Audio with:
    file as "input.wav"
    effects as list containing "noise_reduction", "normalization"
    output_format as "mp3"
```

## 🛠️ **Current Status**

**⚠️ Important Update:** Due to a catastrophic failure during development, our standard libraries are currently being reworked from the ground up. Expected completion: **7-10 days**.

**What's Working Now:**
- ✅ **Complete language parser** - Understands all Runa syntax
- ✅ **Dual syntax system** - Natural and technical syntax fully supported
- ✅ **Core language features** - Variables, functions, control flow, data types
- ✅ **Tooling** - Viewer/developer mode switching
- ✅ **IDE support** - VS Code and Cursor extensions ready

**What's Coming (7-10 days):**
- 🚧 **Universal standard library** - Libraries for every domain
- 🚧 **Runtime environment** - Execute Runa programs
- 🚧 **Package manager** - Install and manage Runa libraries
- 🚧 **Documentation** - Complete guides for every use case

## 🚀 **Getting Started (Right Now)**

### **1. Install the Extension**
- **VS Code**: Search for "Runa Language Support" in Extensions
- **Cursor**: Same extension works in Cursor
- **Other editors**: Coming soon

### **2. Create Your First Runa File**
Create a file with `.runa` extension and start coding:

```runa
Note: My first Runa program!

Let my_name be "World"
Display "Hello, " followed by my_name followed by "!"

Let numbers be list containing 1, 2, 3, 4, 5
Let total be 0

For each number in numbers:
    Set total to total plus number

Display "Sum of numbers: " followed by total

Note: 
This is a multi
line comment
block
:End Note

Process called "example" Note: this is an inline comment
Note: This is a single line comment.
```

### **3. Experience the Magic**
- **Syntax highlighting** - See your code come to life
- **Intelligent completion** - Get suggestions as you type
- **Error detection** - Catch mistakes before they happen
- **Format switching** - Use `--viewer` and `--developer` modes

## 🌐 **The Vision: One Language to Rule Them All**

Runa isn't just another programming language. It's the **end of programming language fragmentation**.

### **Why This Matters:**
- **No more learning 10 languages** for one project
- **Universal code sharing** - Runa code works everywhere
- **AI-native development** - Built for the AI-first future
- **Democratized coding** - Anyone can build anything

### **The Future:**
- **Self-hosting** - Runa will eventually write itself
- **Universal translation** - Convert any code to Runa
- **AI collaboration** - Humans and AIs coding together seamlessly
- **Global accessibility** - Programming in any natural language

## 🎯 **Who Should Use Runa?**

- **Complete beginners** - Start coding without learning cryptic syntax
- **Web developers** - Build full-stack applications in one language
- **Data scientists** - Process data with natural language commands
- **AI researchers** - Create AI systems that understand code naturally
- **Business users** - Automate workflows with readable code
- **Students** - Learn programming concepts without syntax barriers
- **Enterprise teams** - Standardize on one language across all projects

## 🔮 **What's Next?**

1. **Standard libraries complete** (7-10 days)
2. **Runtime environment** (2 weeks)
3. **Package ecosystem** (1 month)
4. **AI integration tools** (2 months)
5. **Self-hosting capability** (6 months)
6. **Universal translation** (1 year)

## 🤝 **Join the Revolution**

Runa is more than a programming language. It's a movement toward **universal programming accessibility**.

- **No more language barriers**
- **No more syntax complexity**
- **No more platform limitations**
- **Just one language for everything**

**Ready to code the future? Start with Runa.**

---

**Runa - The Universal Programming Language**  
*One language. Everything. Everyone.*

*Built with ❤️ by Sybertnetics*
