# GitHub Actions 自动构建指南

本项目已配置GitHub Actions，可以自动构建Windows、macOS和Linux三个平台的可执行文件。

## 🚀 如何使用

### 1. 推送到GitHub

```bash
# 初始化Git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit with GitHub Actions"

# 添加远程仓库
git remote add origin https://github.com/你的用户名/excel-draw-tool.git

# 推送到GitHub
git push -u origin main
```

### 2. 自动构建触发条件

GitHub Actions会在以下情况下自动触发构建：

1. **推送到主分支**：当你推送代码到`main`或`master`分支时
2. **创建Tag**：当你创建一个以`v`开头的标签时（如`v1.0.0`）
3. **Pull Request**：当有人提交Pull Request时
4. **手动触发**：在GitHub仓库的Actions页面手动触发

### 3. 发布新版本

创建一个带版本号的tag并推送：

```bash
# 创建tag
git tag v1.0.0

# 推送tag到GitHub
git push origin v1.0.0
```

这会触发构建并自动创建一个GitHub Release，包含三个平台的可执行文件。

### 4. 手动触发构建

1. 打开你的GitHub仓库
2. 点击 `Actions` 标签
3. 选择 `Build Cross-Platform Binaries` workflow
4. 点击 `Run workflow` 按钮
5. 选择分支并点击 `Run workflow`

## 📦 构建产物

构建完成后，会生成以下文件：

### Windows
- `excel-draw-tool-windows.zip`
  - 包含 `excel-draw-tool.exe` 和所有依赖文件
  - 解压后双击 `excel-draw-tool.exe` 运行
  - 默认访问 `http://localhost:5000`

### macOS
- `excel-draw-tool-macos.tar.gz`
  - 包含 `excel-draw-tool` 可执行文件和依赖
  - 解压后在终端运行：
    ```bash
    tar -xzf excel-draw-tool-macos.tar.gz
    cd excel-draw-tool
    ./excel-draw-tool
    ```

### Linux
- `excel-draw-tool-linux.tar.gz`
  - 包含 `excel-draw-tool` 可执行文件和依赖
  - 解压后在终端运行：
    ```bash
    tar -xzf excel-draw-tool-linux.tar.gz
    cd excel-draw-tool
    ./excel-draw-tool
    ```

## 📥 下载构建产物

### 从Actions下载

1. 打开GitHub仓库的 `Actions` 标签
2. 选择一个成功的workflow运行
3. 在 `Artifacts` 部分下载对应平台的文件

### 从Release下载

如果是通过tag触发的构建：

1. 打开GitHub仓库的 `Releases` 页面
2. 找到对应的版本
3. 在 `Assets` 部分下载对应平台的文件

## 🔧 本地测试构建

### 安装PyInstaller

```bash
source venv/bin/activate
pip install pyinstaller
```

### 构建可执行文件

```bash
# 使用spec文件构建
pyinstaller --clean --noconfirm build.spec

# 构建产物在 dist/excel-draw-tool/ 目录下
```

### 测试可执行文件

```bash
# 运行构建的可执行文件
cd dist/excel-draw-tool
./excel-draw-tool  # macOS/Linux
# 或
excel-draw-tool.exe  # Windows
```

## 📝 构建配置说明

### build.spec 文件

`build.spec` 是PyInstaller的配置文件，定义了：

- **入口文件**：`app.py`
- **包含的数据文件**：
  - `templates/` - HTML模板
  - `sample_defect_data.xlsx` - 示例数据
  - `README.md` - 说明文档
  - `QUICKSTART.md` - 快速开始指南
- **隐式导入**：确保所有依赖都被正确打包
- **输出设置**：创建单个目录包含所有文件

### .github/workflows/build.yml 文件

GitHub Actions工作流配置：

- **多平台构建**：Ubuntu、Windows、macOS
- **Python版本**：3.11
- **自动上传**：构建完成自动上传artifacts
- **Release发布**：tag触发时自动创建release

## ⚙️ 自定义配置

### 修改Python版本

在 `.github/workflows/build.yml` 中修改：

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # 修改这里
```

### 添加更多数据文件

在 `build.spec` 中的 `datas` 列表添加：

```python
datas=[
    ('templates', 'templates'),
    ('sample_defect_data.xlsx', '.'),
    ('README.md', '.'),
    ('你的文件.txt', '.'),  # 添加新文件
],
```

### 修改可执行文件名

在 `build.spec` 中修改：

```python
exe = EXE(
    # ...
    name='excel-draw-tool',  # 修改这里
    # ...
)
```

## 🐛 常见问题

### Q: 构建失败，提示缺少依赖

**解决**：确保 `requirements.txt` 包含所有依赖：

```bash
pip freeze > requirements.txt
```

### Q: 构建的程序运行时找不到模板文件

**解决**：检查 `build.spec` 中的 `datas` 配置，确保模板目录被正确包含。

### Q: macOS上提示"无法打开，因为无法验证开发者"

**解决**：右键点击文件，选择"打开"，然后点击"打开"按钮。

或者在终端运行：
```bash
xattr -cr excel-draw-tool
```

### Q: Linux上提示"权限被拒绝"

**解决**：添加执行权限：
```bash
chmod +x excel-draw-tool
```

### Q: 如何减小可执行文件大小

**解决**：
1. 移除不必要的依赖
2. 在 `build.spec` 中添加 `excludes` 列表
3. 启用UPX压缩（已默认启用）

## 🔒 安全注意事项

1. **不要提交敏感信息**：确保 `.gitignore` 正确配置
2. **GitHub Secrets**：如需API密钥等敏感信息，使用GitHub Secrets
3. **审查依赖**：定期检查和更新依赖包
4. **代码签名**：生产环境建议对可执行文件进行代码签名

## 📚 相关链接

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [PyInstaller文档](https://pyinstaller.org/en/stable/)
- [Python打包指南](https://packaging.python.org/)

## 🎯 最佳实践

1. **版本管理**：使用语义化版本号（如v1.0.0）
2. **变更日志**：在Release中描述版本变更
3. **测试**：本地测试通过后再推送
4. **文档**：保持README和文档更新
5. **备份**：定期备份重要数据

---

**祝构建顺利！** 🚀



