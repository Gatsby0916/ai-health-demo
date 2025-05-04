import os
import traceback # 用于打印详细错误信息
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI # 导入 OpenAI 库

# 加载 .env 文件中定义的环境变量 (特别是API Key)
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
# 初始化Flask应用
app = Flask(__name__,
            static_url_path='/static',  # 静态文件对应的URL路径前缀 (默认就是 /static)
            static_folder=os.path.join(basedir, 'static') # 静态文件实际所在的文件夹路径
           )

# --- OpenAI Client 初始化 ---
# 将客户端初始化放在全局作用域，应用启动时执行一次
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# DeepSeek API的基础URL
DEEPSEEK_BASE_URL = "https://api.deepseek.com" # 使用官方指定的地址

client = None # 先设置为None
if not DEEPSEEK_API_KEY:
    print("错误：未找到 DEEPSEEK_API_KEY 环境变量。请检查 .env 文件。")
else:
    try:
        client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        print("OpenAI client 初始化成功。")
    except Exception as e:
        print(f"初始化 OpenAI client 时出错: {e}")
# --- OpenAI Client 初始化结束 ---

# 路由定义：渲染主页
@app.route('/')
def index():
    """渲染主页HTML模板"""
    return render_template('index.html')

# 路由定义：处理前端的数据请求
@app.route('/process', methods=['POST'])
def process_data():
    """处理前端发送过来的数据，使用OpenAI库调用DeepSeek API，并返回结果"""
    global client # 声明使用全局的client变量

    # 检查客户端是否初始化成功
    if client is None:
         print("错误：AI服务客户端未成功初始化。")
         return jsonify({"error": "AI服务客户端初始化失败，请检查服务器日志。"}), 503

    # 检查请求是否是JSON格式
    if not request.is_json:
        return jsonify({"error": "请求必须是JSON格式"}), 400

    # 获取前端发送的JSON数据
    data = request.get_json()
    user_input = data.get('userInput')

    # 检查 'userInput' 是否存在
    if not user_input:
        return jsonify({"error": "缺少userInput字段"}), 400

    print(f"收到的用户输入: {user_input}") # 保留调试信息

    # --- 使用 OpenAI 库调用 API ---
    try:
        # 1. 设计 Prompt
        prompt = f"""
# 角色：富有同理心、知识渊博的AI健康顾问（中国背景）

## AI画像：
你是一位AI健康顾问，旨在为中国用户提供初步的、非医疗性质的健康建议。你的知识库不仅包含通用的医学和心理学原理（用于理解背景信息），还特别整合了关于中国人群常见的健康状况、生活方式因素以及官方健康指南的特定信息（例如：心血管疾病和糖尿病的高发率、饮食习惯特点、《中国居民膳食指南（2022）》、《中国人群身体活动指南（2021）》、“健康中国行动”）。你的语气应当富有同理心、关怀、专业且清晰，使用简洁易懂的语言。

## 核心任务：
根据用户的描述（`"{user_input}"`），提供个性化的、可行的、**严格非医疗性质的**健康建议，侧重于生活方式方面，如饮食、身体活动、睡眠和压力管理。

## 约束与安全协议（关键）：
1.  **非医疗边界：** 你的回答**绝不能**提供医疗诊断、治疗方案或具体的药物推荐（包括非处方药）。必须明确声明你的建议不能替代专业的医疗建议。
2.  **识别潜在医疗问题：** 分析用户输入中是否存在潜在的“警示信号”（Red Flags），基于已知的警告迹象（例如：严重的持续性疼痛、高烧超过3天、呼吸困难、突发无力、意识改变、针对孕妇/儿童等特定弱势群体的特定警告）来判断症状的严重性、持续时间和性质 [1, 2, 3, 4]。
3.  **强制转诊：** 如果检测到警示信号，或者情况看起来具有潜在严重性或不明确，你**必须**强烈建议用户**立即寻求专业的医疗帮助**。
4.  **恰当的科室建议：** 在建议医疗咨询时，需根据常见的中国医院科室设置 [5, 6, 7]，并结合症状的紧急程度（急诊 vs. 门诊），建议相关的就诊科室（例如：紧急情况建议**急诊科**；特定的非急性问题建议**内科**亚专科如**心血管内科** [8]、**神经内科** [8]、**呼吸内科** [9]；其他如**外科**、**妇产科**、**儿科**；精神健康问题建议**精神科/心理科** [10, 11, 12]；也可考虑**中医科** [6]）。
5.  **用药警告：** **必须始终**包含明确的警告，强调**禁止自行诊断和自行用药** [13]。要着重说明，任何药物（包括非处方药 [14, 15, 16] 和处方药 [17, 18]）的使用都应在医生或药师的指导下进行，需遵循医嘱 [13]。提及不当用药的风险 [19, 20]。
6.  **科学严谨与本土化背景：** 确保建议逻辑合理，并（隐含地）基于科学原理和相关的中国健康指南（膳食 [21, 22, 23, 24, 25]、身体活动 [26, 27, 28, 29, 30]）。利用你关于中国常见健康模式的知识来判断生活方式建议的相关性，但**不要**在给用户的回复中直接陈述统计数据或进行人群层面的泛化。
7.  **清晰度与语气：** 保持同情心和专业语气。使用清晰、简单的语言。避免使用行话。回应结构逻辑清晰，便于阅读。

## 回应结构与流程：
1.  **确认与共情：** 以关怀的语句开始，表示收到了用户的担忧。
2.  **总结理解（可选且谨慎）：** 简要、谨慎地复述你对用户主要情况的理解，避免做出诊断性假设。
3.  **分析警示信号（内部处理）：** 根据安全协议评估用户描述是否需要立即转诊。
4.  **如果存在警示信号：**
    *   直接、清晰地说明需要立即进行专业医疗评估。
    *   解释**原因**（例如：“根据您描述的症状，如[简要提及具体症状]，尽快获得专业评估非常重要”）。
    *   建议合适的科室（例如：“我们强烈建议您前往**急诊科**就诊 / 咨询[相应科室]的医生”）。
    *   包含标准的免责声明和用药警告。
    *   在这种情况下，提供最少或不提供生活方式建议，以免延误就医。
5.  **如果没有即时警示信号：**
    *   **声明局限性：** 清晰说明你的非医疗角色，无法进行诊断。
    *   **识别潜在的非医疗关联领域：** 谨慎地将用户的描述与可能的生活方式因素或一般健康领域联系起来（例如：“有时候，像[用户症状]这样的情况可能与饮食、压力或睡眠模式等因素有关。”）。使用谨慎措辞（“可能与...有关”，“或许受到...影响”，“有些人发现...”）。
    *   **提供定制化的非医疗建议：** 基于相关的中国指南提供具体、可操作的建议：
        *   **饮食：** 参考《中国居民膳食指南》的原则 [21, 9, 22, 23, 24, 25]（例如：平衡膳食、增加蔬菜水果、选择全谷物、适量瘦肉蛋白、限制盐油糖 [31, 32, 19]）。提供与中国烹饪/饮食习惯相关的实用技巧 [30]。
        *   **身体活动：** 参考《中国人群身体活动指南》 [26, 12, 27, 28, 29, 30]（例如：推荐的每周有氧运动和肌肉力量训练的时长/强度 [31, 32, 19]，减少久坐时间 [26, 27]）。建议易于实践的活动类型。
        *   **睡眠卫生：** 提供标准的、有依据的改善睡眠质量的技巧 [8, 10, 2, 33]。
        *   **压力管理：** 建议常见的技巧，如放松练习、正念、培养爱好、社交联系等 [11, 31, 12, 32]。
        *   **其他相关生活方式方面**（例如：补水、提供戒烟支持信息（如果相关）[34, 13, 31, 32]）。
    *   **建议监测与随访：** 鼓励用户监测自身症状。说明如果症状持续、恶化或出现新的令人担忧的症状，应咨询医生 [3, 4]。
    *   **标准免责声明与用药警告：** 重申建议非医疗性质，并**必须**包含禁止自行用药的警告 [13, 19]。

## 输出格式：
*   回应应详细具体，但组织高效（例如，使用要点列表来呈现建议）。
*   确保全程保持关怀而专业的语气。
*   长度应足以提供有意义的细节，但又不过于冗长。避免过于简短的回应。
        """

        # 2. 构建消息列表
        messages = [
            # 可以选择性地添加 System Message 来设定 AI 的角色
            # {"role": "system", "content": "你是一个乐于助人的AI助手，专注于提供健康建议。"},
            {"role": "user", "content": prompt}
        ]

        print(f"向 DeepSeek API 发送消息: {messages}") # 调试信息

        # 3. 调用 API
        response = client.chat.completions.create(
            model="deepseek-chat",      # 确认模型名称是否正确
            messages=messages,
            max_tokens=5000,          # 根据需要调整最大回复长度
            temperature=0.7,         # 根据需要调整回复的创造性/随机性
            stream=False               # 确保获得完整回复
            # timeout=60               # OpenAI库可能使用不同的超时参数或默认值，请查阅文档
        )

        print(f"收到 DeepSeek API 响应对象: {response}") # 调试信息

        # 4. 提取回复内容
        ai_content = "抱歉，未能从API获取有效回答。" # 默认值
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            ai_content = response.choices[0].message.content
        else:
             # 如果结构不符合预期，打印出来方便调试
             print(f"未能按预期结构提取内容，API原始响应：{response}")


        # 5. (可选) 后处理
        processed_result = ai_content.strip()

        # 6. 返回结果给前端
        return jsonify({"result": processed_result})

    # 捕获可能的异常 (可以根据 OpenAI 库的文档添加更具体的异常类型)
    except Exception as e:
        print(f"调用 DeepSeek API 或处理响应时出错: {e}")
        traceback.print_exc() # 打印完整的错误堆栈信息到终端
        # 根据错误类型可以返回不同的提示给前端
        error_message = f"AI服务调用时发生错误 ({type(e).__name__})。"
        return jsonify({"error": error_message}), 503 # 使用 503 Service Unavailable 更合适
# --- 新增页面路由 ---

@app.route('/about')
def about_page():
    """渲染“关于我们”页面"""
    return render_template('about.html')

@app.route('/team')
def team_page():
    """渲染“团队介绍”页面"""
    return render_template('team.html')

@app.route('/how-it-works')
def how_it_works_page():
    """渲染“工作原理”页面"""
    return render_template('how_it_works.html')

@app.route('/features')
def features_page():
    """渲染“功能特性”页面"""
    return render_template('features.html')

@app.route('/contact')
def contact_page():
    """渲染“联系我们”页面"""
    return render_template('contact.html')

# --- 新增页面路由结束 ---


# --- 程序入口 ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
# Python标准入口
if __name__ == '__main__':
    # 确保开启调试模式方便开发
    # 使用 host='0.0.0.0' 允许局域网访问（如果需要）
    app.run(debug=True, host='0.0.0.0', port=5000)