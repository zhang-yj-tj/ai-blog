import os
import json
from typing import Any, Dict, List
from openai import OpenAI
from openai.types.chat.chat_completion import Choice
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis

class MoonshotChat:
    def __init__(self, api_key: str, model_name: str = "moonshot-v1-auto", base_url: str = "https://api.moonshot.cn/v1"):
        """
        初始化 Moonshot Chat 功能。

        :param api_key: Moonshot API 密钥
        :param model_name: 使用的 Moonshot 模型名称（默认为 "moonshot-v1-128k"）
        :param base_url: Moonshot API 的基础 URL 地址
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        执行工具函数。

        这里只是一个示例实现，真正的工具逻辑需要根据需求自定义。
        目前默认直接返回 arguments，作为示例。

        :param tool_name: 工具名称
        :param arguments: 工具调用的参数
        :return: 工具调用的结果
        """
        if tool_name == "$web_search":
            return arguments  # 示例：直接返回参数
        else:
            return f"Error: unable to find tool by name '{tool_name}'"

    def generate_chat_response(self, messages: List[Dict[str, Any]]) -> Choice:
        """
        生成模型的聊天响应。

        :param messages: 对话历史记录
        :return: 模型的响应选择
        """
        completion = self.client。chat。completions。create(
            model=self.model_name，
            messages=messages,
            temperature=0.3，
            tools=[
                {
                    "type": "builtin_function"，
                    "function": {
                        "name": "$web_search"，
                    }，
                }
            ]，
        )
        return completion.choices[0]

    def chat(self, system_description: str, user_question: str) -> str:
        """
        执行完整的聊天流程。

        :param system_description: 系统角色描述
        :param user_question: 用户问题
        :return: 最终的模型回复
        """
        messages = [
            {"role": "system"， "content": system_description}，
            {"role": "user"， "content": user_question}
        ]

        continue_loop = True
        while continue_loop:
            choice = self.generate_chat_response(messages)
            finish_reason = choice.finish_reason

            if finish_reason == "tool_calls":
                messages.append(choice.message)
                for tool_call in choice.message。tool_calls:
                    tool_call_name = tool_call.function。name
                    tool_call_arguments = json.loads(tool_call.function。arguments)

                    tool_result = self.execute_tool(tool_call_name, tool_call_arguments)

                    messages.append({
                        "role": "tool"，
                        "tool_call_id": tool_call.id，
                        "name": tool_call_name,
                        "content": json.dumps(tool_result)，
                    })
            else:
                continue_loop = False

        return choice.message。content

def call_kimi_api(user_question: str, enable_web_search: bool = True) -> str:
    """
    调用 Moonshot Chat 功能。

    :param user_question: 用户问题
    :param system_description: 系统角色描述
    :param api_key: Moonshot API 密钥（默认从环境变量中读取）
    :return: 模型回复
    """
    # 加载 API 密钥
    with open('api.json'， 'r+', encoding='utf-8') as f:
        api_config = json.load(f)
    api_key = api_config[0]["kimi"]
    system_description = "你是一个人工智能助手，请严格我的要求输出。"
    moonshot_client = MoonshotChat(api_key=api_key)
    # 如果启用网络搜索功能，调用 chat 方法时会包含工具调用逻辑
    if enable_web_search:
        return moonshot_client.chat(system_description, user_question)
    else:
        # 如果不启用网络搜索功能，直接生成模型的回复而不调用工具
        messages = [
            {"role": "system"， "content": system_description}，
            {"role": "user"， "content": user_question}
        ]
        completion = moonshot_client.client。chat。completions。create(
            model=moonshot_client.model_name，
            messages=messages,
            temperature=0.3，
        )
        return completion.choices[0]。message。content

def call_deepseek_api(quest):
    with open('api.json'， 'r+', encoding='utf-8') as f:
        api_config = json.load(f)
    api_key = api_config[0]["deepseek"]
    client = OpenAI(api_key = api_key, base_url="https://api.deepseek.com")
    response = client.chat。completions。create(
        model="deepseek-reasoner"，
        messages=[
            {"role": "system"， "content": "你是一个人工智能助手，请帮助我更新网络帖子，下面我将为你提供前置文章和今日娱乐新闻。你需要帮我写后续文章（只输出一章），字数与前置文章相似。"}，
            {"role": "user"， "content": quest}，
        ]，
        stream=False
    )
    return response.choices[0]。message。content

def call_qwen_api(quest):
    from openai import OpenAI
    with open('api.json'， 'r+', encoding='utf-8') as f:
        api_config = json.load(f)
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=api_config[0]["qwen"]，
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"，  # 填写DashScope服务的base_url
    )
    response = client.chat。completions。create(
        model="qwen-plus"，
        messages=[
            {'role': 'system'， 'content': '你是一个人工智能助手，请严格我的要求输出。'}，
            {'role': 'user'， 'content': quest}]
        )
    return response.choices[0]。message。content

def call_photo_api(quest, file_num):
    with open('api.json'， 'r+', encoding='utf-8') as f:
        api_config = json.load(f)
    api_key = api_config[0]["deepseek"]
    client = OpenAI(api_key = api_key, base_url="https://api.deepseek.com")
    response = client.chat。completions。create(
        model="deepseek-chat"，
        messages=[
            {"role": "system"， "content": "你是一个人工智能助手，请帮我输出一个网络帖子封面图的提示词。"}，
            {"role": "user"， "content": quest}，
        ]，
        stream=False
    )
    prompt = response.choices[0]。message。content
    """
    使用指定的提示生成图片，并保存到本地文件。

    参数:
    prompt (str): 用于生成图片的提示。
    file_num (int, 可选): 图片名称中的数字，默认为 1。
    """
    print('图片提示词：'+prompt)
    with open('api.json'， 'r+', encoding='utf-8') as f:
        api_config = json.load(f)
    api_key = api_config[0]["qwen"]
    model = "wanx2.1-t2i-turbo"  # 模型名称
    size = '1024*1024'  # 图片尺寸
    print('图片生成中...请稍候')
    rsp = ImageSynthesis.call(
        api_key=api_key,
        model=model,
        prompt=prompt,
        n=1，  # 生成图片的数量
        size=size
    )
    if rsp.status_code == HTTPStatus.OK:
        # 在当前目录下保存图片
        for result in rsp.output。results:
            file_name = f".\\photo\\{file_num}.png"  # 图片名称中的数字
            with open(file_name, 'wb+') as f:
                f.write(requests.get(result.url)。content)
            print(f"Image saved to {file_name}")
    else:
        print('sync_call Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))
