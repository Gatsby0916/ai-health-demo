# AI个性化健康管理平台 - Demo

本项目是一个基于Web的AI个性化健康管理平台演示版本，旨在为用户提供基于其个人描述的初步健康建议。该平台利用先进的AI模型（通过DeepSeek API）进行智能分析。

<!-- 这里插入 UI.png -->
![平台首页 UI 预览](UI.png "平台首页示例")

## 主要功能

* **用户输入**: 提供简洁的Web界面，方便用户输入健康相关的描述信息。
* **AI分析与建议**: 后端调用 DeepSeek API 对用户输入进行分析，生成个性化的、非医疗性质的健康建议。
* **结果展示**: 在网页上清晰、友好地展示AI生成的分析结果。
* **多页面结构**: 包含首页/Demo、关于我们、工作原理、功能特性、团队介绍、联系我们等页面。
* **交互效果**: 包括导航栏、加载提示动画和结果淡入效果。

## 技术栈

* **后端**: Python, Flask
* **前端**: HTML, CSS, JavaScript
* **AI 服务**: DeepSeek API (通过 `openai` Python 库调用)
* **模板引擎**: Jinja2
* **环境管理**: Python Virtual Environment (`venv`)
* **API Key管理**: `python-dotenv`
* **Markdown渲染 (前端)**: `marked.js` (可选，如果前端处理Markdown)

## 项目结构

```
health_ai_demo/
│
├── static/              # 存放 CSS, JS, Images 等静态文件
│   ├── style.css
│   ├── script.js
│   └── images/
│       ├── logo.png         (示例)
│       ├── icon_*.png       (示例)
│       └── member_*.jpg     (示例)
│
├── templates/           # 存放 HTML 模板文件
│   ├── base.html          # 基础模板
│   ├── index.html         # 首页/Demo页
│   ├── about.html         # 关于我们
│   ├── how_it_works.html  # 工作原理
│   ├── features.html      # 功能特性
│   ├── team.html          # 团队介绍
│   ├── contact.html       # 联系我们
│   └── footer_content.html (可选，页脚内容)
│
├── venv/                # Python 虚拟环境文件夹 (通常不提交到Git)
├── __pycache__/         # Python 缓存文件夹 (通常不提交到Git)
│
├── .env                 # 存放环境变量，如API Key (不提交到Git)
├── .gitignore           # 指定Git忽略的文件和文件夹
├── app.py               # Flask 应用主文件
├── requirements.txt     # Python 依赖库列表
└── README.md            # 项目说明文件 (就是本文件)

```

## 安装与设置

1.  **克隆仓库 (如果使用Git)**
    ```bash
    git clone [您的仓库地址]
    cd health_ai_demo
    ```
2.  **创建并激活Python虚拟环境**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  **安装依赖**
    * (推荐) 先确保您已根据项目情况生成了 `requirements.txt` 文件:
        ```bash
        pip freeze > requirements.txt
        ```
    * 然后安装依赖:
        ```bash
        pip install -r requirements.txt
        ```
4.  **配置环境变量**
    * 在项目根目录创建 `.env` 文件。
    * 在 `.env` 文件中添加以下行，并将 `Your_Key_Here` 替换为您真实的 DeepSeek API Key：
        ```plaintext
        DEEPSEEK_API_KEY='Your_Key_Here'
        ```

## 运行项目

1.  **确保虚拟环境已激活** (终端提示符前有 `(venv)`)。
2.  **运行Flask应用**：
    ```bash
    flask run
    ```
3.  **访问应用**：在浏览器中打开终端提示的地址，通常是 `http://127.0.0.1:5000`。

## 团队成员

* **李海毅**: [项目负责人 / 产品设计] | 电话: +61 0416789927 | 邮箱: lihaiyi2003@outlook.com


## 注意事项

* 本应用提供的健康建议仅供参考，不能替代专业的医疗诊断和建议。
* 请妥善保管您的 DeepSeek API Key，不要公开分享或提交到代码仓库。

