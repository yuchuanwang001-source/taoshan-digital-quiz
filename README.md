# 淘闪数智·刷题系统

淘宝闪购数智经营生态基础知识刷题工具，帮助运营人员快速掌握 CRM、TRUST 模型、品牌店功能和品牌案例等核心知识。

🔗 **在线地址：** https://yuchuanwang001-source.github.io/taoshan-digital-quiz/

## 功能

- 160 道专业题库（选择题+判断题），覆盖 4 大知识模块
- 每次随机抽 50 题，选项顺序打乱
- 30 秒倒计时，模拟考试压力
- 交卷自动评分 + 错题解析
- 支持成绩同步到钉钉群

## 使用方法

**在线访问：** 打开上面的链接直接做题，无需安装任何软件。

**本地运行：**
```bash
# 方式一：双击 start.bat（Windows）
# 方式二：命令行
python server.py
# 浏览器打开 http://localhost:8000
```

## 项目结构

```
├── index.html          # 主页面（含完整前端逻辑）
├── questions.js        # 题库（160题）
├── server.py           # 本地HTTP服务器 + 钉钉代理
├── start.bat           # Windows一键启动
└── .gitignore
```

## 技术栈

HTML + CSS + JavaScript（纯前端，无框架依赖）
