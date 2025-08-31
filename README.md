# travel-agent-minimal

前后端最小可运行骨架 + **真实高德(Amap)调用**：
- 前端：Vite + Vue3
- 后端：FastAPI + httpx
- 仅 1 个接口 `/api/plan`，根据兴趣关键字调用 **高德Web服务**（地理编码、POI 关键字搜索、步行/驾车/公交路径规划），返回行程 JSON。

> 默认直连高德 Web Service（REST）；如你后续部署了 MCP server，也可在 `services/gaode_mcp.py` 中扩展 MCP 调用逻辑。

## ✨ 主要功能

- 🗺️ **智能景点推荐**: 基于兴趣关键词自动搜索相关景点
- 📍 **地理编码**: 支持起点设置，自动获取坐标
- 🚶 **路径规划**: 计算景点间移动时间和距离
- 📅 **行程安排**: 按天分配景点，支持不同节奏设置
- 🔍 **调试信息**: 详细的日志和调试信息，便于问题排查
- 🎯 **兴趣分类**: 预设8大类兴趣，支持自定义关键词

## 🚀 本地运行

### 1. 环境准备

确保已安装：
- Python 3.8+
- Node.js 16+
- 高德地图API密钥

### 2. 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp ../.env.example .env  # 填写你的 GAODE_API_KEY

# 启动服务
uvicorn app.main:app --reload --port 8000
```

### 3. 前端启动

```bash
cd frontend
npm i
npm run dev
```

访问输出的本地地址（通常 http://localhost:5173/ ）

## 🔑 获取高德地图API密钥

1. 访问 [高德开放平台](https://lbs.amap.com/)
2. 注册账号并登录
3. 创建应用，选择"Web服务"类型
4. 获取API Key并填入 `.env` 文件

## 🧪 测试验证

### 后端测试
```bash
cd backend
python test_api.py
```

### 前端测试
1. 使用常见城市名称（如：北京、上海、杭州）
2. 选择1-3天的短行程进行测试
3. 尝试不同的兴趣组合（如：history,food 或 nature,shopping）

## 🔧 常见问题解决

### 景点推荐为空

**可能原因：**
- API密钥未设置或无效
- 城市名称不正确
- 网络连接问题

**解决方法：**
- 检查 `.env` 文件中的 `GAODE_API_KEY` 是否正确设置
- 确保城市名称使用中文（如：北京、上海、广州）
- 查看后端日志获取详细错误信息

### API调用失败

**可能原因：**
- API密钥超出使用限制
- 请求参数错误
- 高德服务暂时不可用

**解决方法：**
- 检查API使用量是否超限
- 查看后端日志获取详细错误信息
- 稍后重试

## 📁 项目结构

```
travel-agent-minimal/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── core/           # 配置管理
│   │   ├── routers/        # API路由
│   │   ├── schemas/        # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── requirements.txt     # Python依赖
│   └── test_api.py         # 测试脚本
├── frontend/                # 前端应用
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   ├── pages/          # 页面组件
│   │   └── api/            # API调用
│   └── package.json        # Node.js依赖
└── README.md               # 项目说明
```

## 🎯 兴趣分类

系统预设了8大类兴趣，每类包含多个相关关键词：

- **历史文化**: 博物馆、古迹、故宫、长城等
- **艺术展览**: 美术馆、艺术中心、画廊等
- **自然风光**: 公园、山、湖、风景区等
- **美食小吃**: 小吃、美食街、老字号等
- **购物娱乐**: 商场、步行街、购物中心等
- **娱乐休闲**: 游乐园、电影院、剧院等
- **宗教建筑**: 寺庙、教堂、清真寺等
- **教育科技**: 大学、图书馆、科技馆等

## 📝 开发说明

### 后端扩展
- 在 `services/gaode_mcp.py` 中添加新的高德API调用
- 在 `utils/itinerary.py` 中优化行程规划算法
- 在 `schemas/plan.py` 中扩展数据模型

### 前端扩展
- 在 `components/` 中添加新的UI组件
- 在 `pages/` 中创建新的页面
- 在 `api/` 中添加新的接口调用

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## �� 许可证

MIT License
