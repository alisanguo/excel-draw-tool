from flask import Flask, request, render_template, jsonify
import os
import pandas as pd
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = 'your-secret-key-here'

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 状态映射规则
STATUS_MAPPING = {
    '新建': '待修复',
    '修复中': '待修复',
    '待修复': '待修复',
    '待解决': '待修复',  # 兼容不同命名
    '处理中': '待修复'   # 兼容不同命名
}

def apply_status_mapping(df):
    """
    应用状态映射规则：新建、修复中、待修复 → 统一映射为待修复
    """
    if '状态' in df.columns:
        df['原始状态'] = df['状态']
        df['状态'] = df['状态'].map(lambda x: STATUS_MAPPING.get(x, x))
    return df

def analyze_defect_data(df, selected_modules=None):
    """
    根据缺陷数据生成统计分析
    按照图片中的统计规则实现
    """
    # 应用状态映射
    df = apply_status_mapping(df)
    
    # 如果指定了模块过滤
    if selected_modules and '缺陷模块' in df.columns:
        df = df[df['缺陷模块'].isin(selected_modules)]
    
    stats = {}
    current_date = datetime.now()
    
    # 1. 不同状态下，统计缺陷数量【count(标题)】
    if '状态' in df.columns and '标题' in df.columns:
        status_count = df.groupby('状态')['标题'].count().to_dict()
        stats['status_count'] = status_count
    
    # 2. 缺陷停留时长
    # 统计状态为待修复的缺陷（新建、修复中、待修复等已映射为待修复）
    # 停留时长 = 当前时间所在天 - 创建时间所在天（单位：天）
    if '状态' in df.columns and '创建时间' in df.columns and '标题' in df.columns:
        # 筛选状态为'待修复'的缺陷（包括映射后的新建、修复中等）
        pending_defects = df[df['状态'] == '待修复'].copy()
        if len(pending_defects) > 0:
            # 解析创建时间为日期
            pending_defects['创建时间_dt'] = pd.to_datetime(pending_defects['创建时间'], errors='coerce')
            # 计算停留天数：当前日期 - 创建日期
            pending_defects['停留天数'] = pending_defects['创建时间_dt'].apply(
                lambda x: (current_date.date() - x.date()).days if pd.notna(x) else None
            )
            # 过滤掉None值（创建时间解析失败的）
            pending_defects = pending_defects[pending_defects['停留天数'].notna()]
            # 按停留天数分组，统计每个天数对应的缺陷数量
            if len(pending_defects) > 0:
                stay_duration = pending_defects.groupby('停留天数')['标题'].count().to_dict()
                stats['stay_duration'] = {str(int(k)): int(v) for k, v in stay_duration.items()}
            else:
                stats['stay_duration'] = {}
        else:
            stats['stay_duration'] = {}
    else:
        stats['stay_duration'] = {}
    
    # 3. 每日新增/修复缺陷情况
    daily_stats = {}
    
    # 每日新增：创建时间为对应天的缺陷数量
    if '创建时间' in df.columns and '标题' in df.columns:
        df_copy = df.copy()
        # 将创建时间转换为日期（去掉时分秒）
        df_copy['创建日期'] = pd.to_datetime(df_copy['创建时间'], errors='coerce').dt.date
        # 按创建日期分组统计缺陷数量
        daily_new = df_copy.groupby('创建日期')['标题'].count().to_dict()
        daily_stats['daily_new'] = {str(k): int(v) for k, v in sorted(daily_new.items()) if k is not None}
    else:
        daily_stats['daily_new'] = {}
    
    # 每日修复：待验证状态且更新时间为对应天 + 已关闭状态且完成时间为对应天
    daily_fixed = {}
    
    # 1) 待验证状态的缺陷，使用更新时间
    if '状态' in df.columns and '更新时间' in df.columns and '标题' in df.columns:
        pending_verify = df[df['状态'] == '待验证'].copy()
        if len(pending_verify) > 0:
            # 将更新时间转换为日期
            pending_verify['更新日期'] = pd.to_datetime(pending_verify['更新时间'], errors='coerce').dt.date
            # 按更新日期统计
            for date, count in pending_verify.groupby('更新日期')['标题'].count().items():
                if pd.notna(date):
                    daily_fixed[date] = daily_fixed.get(date, 0) + int(count)
    
    # 2) 已关闭状态的缺陷，使用完成时间
    if '状态' in df.columns and '完成时间' in df.columns and '标题' in df.columns:
        closed = df[df['状态'] == '已关闭'].copy()
        if len(closed) > 0:
            # 将完成时间转换为日期
            closed['完成日期'] = pd.to_datetime(closed['完成时间'], errors='coerce').dt.date
            # 按完成日期统计
            for date, count in closed.groupby('完成日期')['标题'].count().items():
                if pd.notna(date):
                    daily_fixed[date] = daily_fixed.get(date, 0) + int(count)
    
    daily_stats['daily_fixed'] = {str(k): int(v) for k, v in sorted(daily_fixed.items())}
    stats['daily_stats'] = daily_stats
    
    # 4. 缺陷分析归类统计（饼图）
    if '缺陷分析类型' in df.columns:
        analysis_count = df['缺陷分析类型'].value_counts().to_dict()
        stats['analysis_type_count'] = analysis_count
    
    return stats

def get_module_list(df):
    """
    获取缺陷模块列表（去重）
    """
    if '缺陷模块' in df.columns:
        modules = df['缺陷模块'].dropna().unique().tolist()
        return sorted(modules)
    return []

# 存储上传的文件数据（临时存储）
uploaded_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """上传文件并返回模块列表"""
    if 'file' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if not file.filename.endswith('.xlsx'):
        return jsonify({'error': '请上传Excel文件(.xlsx格式)'}), 400
    
    try:
        # 保存上传的文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"defect_data_{timestamp}.xlsx"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 读取Excel文件
        df = pd.read_excel(filepath)
        
        # 获取模块列表
        modules = get_module_list(df)
        
        # 存储数据（使用timestamp作为key）
        uploaded_data[timestamp] = {
            'filepath': filepath,
            'dataframe': df,
            'modules': modules
        }
        
        return jsonify({
            'success': True,
            'timestamp': timestamp,
            'modules': modules,
            'total_records': len(df)
        })
        
    except Exception as e:
        return jsonify({'error': f'处理文件时出错: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze_data():
    """根据选择的模块分析数据并返回图表数据"""
    try:
        data = request.json
        timestamp = data.get('timestamp')
        selected_modules = data.get('modules', [])
        
        if not timestamp or timestamp not in uploaded_data:
            return jsonify({'error': '数据不存在或已过期'}), 400
        
        # 获取存储的数据
        df = uploaded_data[timestamp]['dataframe'].copy()
        
        # 如果没有选择模块，使用全部模块
        if not selected_modules:
            selected_modules = uploaded_data[timestamp]['modules']
        
        # 生成统计数据
        stats = analyze_defect_data(df, selected_modules)
        
        # 转换为JSON可序列化的格式
        result = {
            'success': True,
            'stats': stats,
            'selected_modules': selected_modules,
            'filtered_records': len(df[df['缺陷模块'].isin(selected_modules)]) if '缺陷模块' in df.columns else len(df)
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'分析数据时出错: {str(e)}'}), 500

if __name__ == '__main__':
    import sys
    import socket
    import webbrowser
    from datetime import datetime
    
    # 创建日志目录
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置日志文件
    log_file = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    def log(message):
        """记录日志到文件和控制台"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f'[{timestamp}] {message}'
        print(log_message)
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except:
            pass
    
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
    
    try:
        log('='*60)
        log('Excel缺陷数据统计分析工具启动中...')
        log('='*60)
        
        # 检查端口
        port = 5000
        if not check_port(port):
            log(f'警告: 端口 {port} 已被占用，尝试使用其他端口...')
            for test_port in range(5001, 5010):
                if check_port(test_port):
                    port = test_port
                    log(f'使用端口: {port}')
                    break
            else:
                log('错误: 无法找到可用端口 (5000-5009 都被占用)')
                log('请关闭其他占用端口的程序后重试')
                input('\n按回车键退出...')
                sys.exit(1)
        
        log(f'启动Web服务器...')
        log(f'访问地址: http://localhost:{port}')
        log(f'日志文件: {log_file}')
        log('='*60)
        log('服务器运行中... 按 Ctrl+C 停止服务')
        log('='*60)
        
        # 自动打开浏览器
        try:
            webbrowser.open(f'http://localhost:{port}')
            log('已自动打开浏览器')
        except:
            log('无法自动打开浏览器，请手动访问上述地址')
        
        # 启动Flask应用
        app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)
        
    except KeyboardInterrupt:
        log('\n服务器已停止')
    except Exception as e:
        log(f'错误: {str(e)}')
        log(f'详细错误信息: {repr(e)}')
        import traceback
        log('完整错误堆栈:')
        log(traceback.format_exc())
        log('='*60)
        log('程序遇到错误，请查看上述日志信息')
        log(f'日志已保存到: {log_file}')
        input('\n按回车键退出...')
        sys.exit(1)

