# 小红书内容自动化生成系统 / Xiaohongshu content automatic generation system

## 🌟 项目定位 / **Project Vision**

- 专注于小红书平台的智能化内容生产解决方案，通过多阶段AI协同工作流实现从热点追踪到合规发布的完整闭环，特别针对平台特性优化内容安全性和传播效果。
- An intelligent content production system optimized for Xiaohongshu platform, featuring multi-stage AI collaboration workflow with built-in compliance safeguards.

## ⬆️ 开始使用 / **Start Using**
### 使用方法 / **Usage**

**先决条件:正确安装浏览器及对应的`webdriver`，并添加到系统变量**

**Prerequisites: Install the browser and corresponding `webdriver` correctly, and add it to the system variables.**

1. **配置`config.json`配置文件和`api.json`密钥文件，并将你前期更新的1-2篇文章放入`articles.json`**  
   - **Configure the `config.json` configuration file and the `api.json` key file, and place your 1-2 initial articles in the `articles.json` file.**

2. **运行`main`文件，即可获取输出（文章会输出在控制台，图片会输出在`photo`文件夹）**  
   - **Run the `main` file to get the output (articles will be displayed in the console, and images will be saved in the `photo` folder).**

### 实践案例 / **Practical Case**

- **本项目作者亲测稳定运行，欢迎关注小红书号：`3862445530`**  
  - **The project author has tested it and it runs stably. Follow my Xiaohongshu account: `3862445530`**

## 🔄 核心工作流 / **Core Workflow**

1. **热点捕获 / Trend Monitoring**
   - 从微博文娱榜获取实时热搜数据  
   - Scrape real-time hot search data from Weibo's entertainment chart  
2. **信息增强 / Context Expansion**
   - 调用Kimi AI联网检索补充事件细节  
   - Use Kimi AI to search online and enhance event details  
3. **风格学习 / Style Modeling** 
   - 分析历史文章建立内容模型  
   - Analyze historical posts to build a content model  
4. **初稿生成 / Draft Generation** 
   - DeepSeek-R1模型创作优质内容  
   - Generate high-quality content using DeepSeek-R1 model  
5. **安全检测 / Compliance Scan** 
   - 零克查词平台敏感词扫描  
   - Scan for sensitive words using Lingke's detection platform  
6. **智能降敏 / Optimization** 
   - Qwen AI多轮迭代优化（≤2次）  
   - Iterative optimization by Qwen AI (up to 2 times)  
7. **最终处理 / Final Processing** 
   - 顽固敏感词转拼音
   - Convert stubborn sensitive words to pinyin
8. **视觉生成 / Visual Creation** 
   - DeepSeek-V3生成提示词 → Qwen-VL生成封面  
   - DeepSeek-V3 generates prompts → Qwen-VL creates cover images  
9. **发布准备 / Publishing** 
   - 自动添加`#标签`并提示用户发布 （⚠️注意：此功能存在非核心漏洞，可能在粘贴发布时无法识别为标签，将在后续版本修复）
   - Automatically add `#tags` and prompt user to publish  (⚠️ Note: This feature has a non-core vulnerability, which may not be recognized as a label when pasted for release, and will be fixed in subsequent versions)

## 🚀 核心优势 / **Key Advantages**

- **三重安全屏障 / Triple Safety**：
  - AI改写 → 拼音替换 → 人工确认  
  - AI rewriting → Pinyin masking → Manual confirmation  
- **跨平台数据融合 / Cross-platform Data**：
  - 微博热点 + 小红书风格 + 专业审核  
  - Weibo trends + Xiaohongshu style + professional review  
- **成本优化 / Cost Efficiency**：
  - 高低价AI模型协同作业  
  - Collaborative use of high- and low-cost AI models  
- **智能记忆 / Adaptive Learning**：建立持续进化的内容风格库  
  - 建立持续进化的内容风格库  
  - Build an evolving content style database  
- **风险管控 / Risk Control**：
  - 敏感词阈值预警机制  
  - Sensitive word threshold alert mechanism  

## 🛠️ 技术架构 / **Tech Architecture**

| 功能模块 / Module | 技术方案 / Solution |
|-------------------|---------------------|
| 热搜数据采集 / Data Collection | Selenium动态渲染 + XPath解析 / Selenium dynamic rendering + XPath parser |
| 内容生成 / Content Generation | DeepSeek-R1 + 风格迁移学习 / DeepSeek-R1 + style transfer |
| 敏感词处理 / Compliance | 零克平台检测 + Qwen-Turbo优化 / Lingke platform + Qwen-Turbo |
| 多模态生成 / Multimodal | DeepSeek-V3提示工程 + Qwen-VL绘图 / DeepSeek-V3 prompts → Qwen-VL imaging |

## ⚙️ 配置参数 / **Configuration**

| 参数项 / Parameter | 说明 / Description | 建议值 / Recommended |
|---------------------|---------------------|-----------------------|
| 热点获取数量 / Hot Trends | 每次分析的微博热搜条目数 / Weibo trends per cycle | 3-5 |
| 历史学习深度 / History Depth | 参考的历史爆文数量 / Reference posts for style | 5-8 |
| 内容垂直领域 / Content Category | 娱乐/美妆/时尚等分类 / Entertainment/Beauty/Fashion | 需明确 / Required |
| 字数偏离 / Word Deviation | 文章输出的字数与历史文章均值的偏离率限制 / Deviation Rate Limit between the Number of Words Output of Articles and the Mean of Historical Articles | 0.4-0.7 |

## 📅 版本演进 / **Roadmap**

- **现役版本 / active version (v1.0)**  
  - **完整文章自动化生产检测流程 / Full article automated production inspection process**  
  - **跨平台内容安全适配 / Cross-platform adaptation**  
- **开发中版本 / development version (v2.0)**  
  - **小红书自动发布接口（⚠️警告：此操作有封号风险） / Auto-publish interface (⚠️Warning: There is a risk of ban in this operation)**  
  - **流量高峰预测系统 / Traffic prediction system**  
- **规划版本 / planning version (v3.0)**  
  - **爆文概率预测模型 / Viral prediction model**  
  - **历史文章火爆程度分析 / Analysis of the popularity of historical articles**  

## 📬 联系作者 / Contact

- **电子邮箱 / Email**: `zhang.ershi@qq.com`  
- **微信号 / WeChat**: `zhang_tjnk`  
