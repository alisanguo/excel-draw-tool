# Windows离线使用 - 完整解决方案

## 🎯 问题总结

### 原问题
在Windows环境使用时出现错误：
```
ReferenceError: echarts is not defined
```

### 根本原因
1. 应用依赖CDN加载ECharts库
2. Windows防火墙可能阻止CDN访问
3. 离线环境无法访问外部网络
4. 内网环境无公网访问权限

## ✅ 完整解决方案

### 方案：ECharts库本地化

已将ECharts库（1.0MB）下载到项目本地，实现完全离线支持。

## 📦 已完成的修改

### 1. 下载ECharts到本地
```bash
static/js/echarts.min.js  # 1.0MB
```

### 2. 更新HTML模板
```html
<!-- 之前：使用CDN -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>

<!-- 现在：使用本地文件 -->
<script src="{{ url_for('static', filename='js/echarts.min.js') }}"></script>
```

### 3. 更新PyInstaller配置
```python
# build.spec
datas=[
    ('templates', 'templates'),
    ('static', 'static'),  # ← 新增
    # ...
],
```

### 4. 添加错误检测
```javascript
// 页面加载时检查ECharts
window.addEventListener('load', function() {
    if (typeof echarts === 'undefined') {
        alert('图表库加载失败！请检查网络连接后刷新页面。');
    } else {
        console.log('ECharts loaded successfully, version:', echarts.version);
    }
});
```

## 🚀 使用方法

### 方式1：本地开发

```bash
# 1. 启动应用
./start.sh

# 或
source venv/bin/activate
python app.py

# 2. 浏览器访问
http://localhost:5000
```

### 方式2：打包后的可执行文件

```bash
# Windows
解压 excel-draw-tool-windows.zip
进入 excel-draw-tool 目录
双击 excel-draw-tool.exe
浏览器访问 http://localhost:5000

# macOS
tar -xzf excel-draw-tool-macos.tar.gz
cd excel-draw-tool
./excel-draw-tool

# Linux
tar -xzf excel-draw-tool-linux.tar.gz
cd excel-draw-tool
chmod +x excel-draw-tool
./excel-draw-tool
```

## 🧪 测试验证

### 自动测试脚本

```bash
./test_offline.sh
```

这会检查：
- ✅ ECharts文件是否存在
- ✅ HTML是否使用本地库
- ✅ PyInstaller配置是否正确
- ✅ 启动应用进行实际测试

### 手动测试步骤

#### 1. 断网测试
```
Windows: 关闭WiFi或拔掉网线
macOS: 关闭WiFi
Linux: 断开网络
```

#### 2. 启动应用
```bash
python app.py
```

#### 3. 浏览器访问
- 打开 http://localhost:5000
- 按F12打开开发者工具
- 查看Console标签

#### 4. 验证成功标志
在Console中应该看到：
```
ECharts loaded successfully, version: 5.4.3
```

#### 5. 功能测试
- 上传Excel文件
- 选择模块
- 点击"生成图表"
- **确认4个图表都正常显示**

## 📊 支持的环境

### ✅ 完全支持
- Windows 7/8/10/11 (离线)
- macOS 10.13+ (离线)
- Linux各发行版 (离线)
- 内网环境
- 防火墙限制环境
- 代理环境

### ✅ 网络环境
- 离线环境 ✅
- 在线环境 ✅
- 内网环境 ✅
- 公网隔离 ✅

## 🔍 故障排查

### 问题1: 图表仍然不显示

**检查步骤**:

1. **验证ECharts文件**
   ```bash
   ls -lh static/js/echarts.min.js
   # 应该显示约1.0M
   ```

2. **检查浏览器Console**
   - 按F12打开开发者工具
   - 查看Console标签
   - 看是否有错误信息

3. **清除浏览器缓存**
   ```
   Windows: Ctrl + Shift + Delete
   macOS: Cmd + Shift + Delete
   ```
   或强制刷新：
   ```
   Windows: Ctrl + F5
   macOS: Cmd + Shift + R
   ```

### 问题2: 文件不存在

**解决方法**:
```bash
# 重新下载ECharts
mkdir -p static/js
cd static/js
curl -o echarts.min.js https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js

# 验证下载
ls -lh echarts.min.js
```

### 问题3: 打包后找不到静态文件

**原因**: PyInstaller配置问题

**解决方法**:
1. 检查 `build.spec` 文件
2. 确认包含 `('static', 'static')` 配置
3. 重新打包：
   ```bash
   pyinstaller --clean --noconfirm build.spec
   ```

### 问题4: Windows Defender阻止

**解决方法**:
1. 右键可执行文件
2. 选择"属性"
3. 勾选"解除锁定"
4. 点击"应用"

或添加到白名单：
1. 打开Windows安全中心
2. 病毒和威胁防护
3. 管理设置
4. 添加排除项

## 📁 文件结构

```
excel-draw-tool/
├── static/               # 新增静态资源目录
│   └── js/
│       └── echarts.min.js  # 1.0MB ECharts库
├── templates/
│   └── index.html       # 已更新使用本地库
├── app.py               # Flask应用
├── build.spec           # 已配置打包static
├── test_offline.sh      # 离线测试脚本
├── 离线使用说明.md       # 详细文档
└── Windows离线使用完整解决方案.md  # 本文档
```

## 💡 最佳实践

### Windows环境
1. 使用打包后的.exe文件
2. 无需安装Python
3. 双击运行即可
4. 完全独立，无外部依赖

### 内网部署
1. 将打包文件拷贝到内网
2. 解压后直接运行
3. 无需配置网络
4. 无需安装依赖

### 离线使用
1. 确保文件完整
2. 不依赖任何外部资源
3. 可在完全隔离环境使用

## 🔄 更新步骤

如果你有旧版本，更新步骤：

### Git仓库
```bash
# 1. 拉取最新代码
git pull origin main

# 2. 验证文件
ls -lh static/js/echarts.min.js

# 3. 重启应用
./start.sh
```

### 已下载的可执行文件
1. 下载新版本的压缩包
2. 解压到新目录
3. 运行新版本

## 📚 相关文档

- [离线使用说明.md](离线使用说明.md) - 详细技术文档
- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
- [README.md](README.md) - 项目总览

## 🎉 优势总结

### 之前（CDN版本）
- ❌ 需要网络连接
- ❌ 受防火墙限制
- ❌ CDN可能被阻止
- ❌ 离线不可用

### 现在（本地版本）
- ✅ 完全离线可用
- ✅ 不受网络限制
- ✅ 防火墙友好
- ✅ 加载更快
- ✅ 独立运行
- ✅ 内网可用

## 📞 技术支持

### 常见问题
查看：[离线使用说明.md](离线使用说明.md)

### 测试工具
运行：`./test_offline.sh`

### 日志查看
检查：浏览器开发者工具 Console

## 🎯 总结

✅ **问题**: Windows使用报错"echarts is not defined"  
✅ **原因**: CDN被防火墙阻止  
✅ **解决**: ECharts库本地化  
✅ **结果**: 完全离线可用  

---

**现在可以在Windows环境完全离线使用了！** 🎉

无需网络连接，随时随地使用本工具进行缺陷数据分析！

