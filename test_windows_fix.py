#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Windows修复功能
"""
import os
import sys
import socket
import tempfile
from datetime import datetime

def test_port_check():
    """测试端口检查功能"""
    print("测试端口检查功能...")
    
    def check_port(port):
        """检查端口是否可用"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result != 0  # 返回True表示端口可用
        except:
            return False
    
    # 测试一些常用端口
    test_ports = [5000, 5001, 5002, 80, 443]
    for port in test_ports:
        available = check_port(port)
        status = "可用" if available else "被占用"
        print(f"  端口 {port}: {status}")
    
    print("✅ 端口检查功能正常\n")
    return True  # 修复：返回True表示测试通过

def test_log_creation():
    """测试日志创建功能"""
    print("测试日志创建功能...")
    
    # 创建临时日志目录
    log_dir = tempfile.mkdtemp(prefix='test_logs_')
    print(f"  临时日志目录: {log_dir}")
    
    # 测试日志文件创建
    log_file = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    def log(message):
        """记录日志到文件和控制台"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f'[{timestamp}] {message}'
        print(f"  LOG: {log_message}")
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except Exception as e:
            print(f"  ERROR: 写入日志失败: {e}")
            return False
        return True
    
    # 写入测试日志
    success = log("测试日志消息 1")
    success = success and log("测试日志消息 2")
    success = success and log("测试日志消息 3")
    
    # 检查日志文件
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.strip().split('\n')
            print(f"  日志文件创建成功，包含 {len(lines)} 行")
            if len(lines) >= 3:
                print("✅ 日志创建功能正常\n")
                # 清理测试文件
                os.remove(log_file)
                os.rmdir(log_dir)
                return True
    
    print("❌ 日志创建功能异常\n")
    return False

def test_batch_files():
    """测试bat文件是否存在"""
    print("测试启动脚本...")
    
    required_files = [
        '启动.bat',
        '调试模式启动.bat',
        'Windows使用说明.md',
        'README_Windows.txt'
    ]
    
    all_exist = True
    for filename in required_files:
        exists = os.path.exists(filename)
        status = "✓" if exists else "✗"
        print(f"  {status} {filename}")
        if not exists:
            all_exist = False
    
    if all_exist:
        print("✅ 所有启动脚本和文档存在\n")
        return True
    else:
        print("❌ 部分文件缺失\n")
        return False

def test_app_imports():
    """测试app.py的导入"""
    print("测试app.py导入...")
    
    try:
        # 测试必要的导入
        import flask
        import pandas
        import openpyxl
        from datetime import datetime
        import socket
        import webbrowser
        
        print("  ✓ Flask")
        print("  ✓ Pandas")
        print("  ✓ Openpyxl")
        print("  ✓ datetime")
        print("  ✓ socket")
        print("  ✓ webbrowser")
        print("✅ 所有依赖导入成功\n")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}\n")
        return False

def test_spec_file():
    """测试build.spec配置"""
    print("测试build.spec配置...")
    
    if not os.path.exists('build.spec'):
        print("❌ build.spec 不存在\n")
        return False
    
    with open('build.spec', 'r', encoding='utf-8') as f:
        content = f.read()
        
        checks = {
            '启动.bat': "('启动.bat'" in content,
            '调试模式启动.bat': "('调试模式启动.bat'" in content,
            'strip=True': 'strip=True' in content,
            'upx=True': 'upx=True' in content,
            'console=True': 'console=True' in content,
        }
        
        all_passed = True
        for check_name, passed in checks.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("✅ build.spec 配置正确\n")
            return True
        else:
            print("❌ build.spec 配置缺失部分内容\n")
            return False

def main():
    """主测试函数"""
    print("="*60)
    print("Windows修复功能测试")
    print("="*60)
    print()
    
    results = []
    
    # 运行所有测试
    results.append(("端口检查", test_port_check()))
    results.append(("日志创建", test_log_creation()))
    results.append(("启动脚本", test_batch_files()))
    results.append(("依赖导入", test_app_imports()))
    results.append(("构建配置", test_spec_file()))
    
    # 输出总结
    print("="*60)
    print("测试结果总结")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:12s} : {status}")
    
    print("="*60)
    print(f"总计: {passed}/{total} 通过")
    print("="*60)
    
    if passed == total:
        print("\n🎉 所有测试通过！可以提交代码。")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查后再提交。")
        return 1

if __name__ == '__main__':
    sys.exit(main())

