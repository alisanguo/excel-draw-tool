from flask import Flask, request, render_template, jsonify
import os
import pandas as pd
from datetime import datetime, timedelta
import json
import re

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
    创建映射后的状态列，保留原始状态列用于其他统计
    """
    if '状态' in df.columns:
        # 保留原始状态（用于状态统计、每日修复等）
        if '原始状态' not in df.columns:
            df['原始状态'] = df['状态']
        # 创建映射后的状态列（用于缺陷停留时长统计）
        df['映射后状态'] = df['原始状态'].map(lambda x: STATUS_MAPPING.get(x, x))
    return df

def analyze_defect_data(df, selected_modules=None, selected_statuses=None, classification_mode='manual', keywords=None):
    """
    根据缺陷数据生成统计分析
    按照图片中的统计规则实现
    
    Args:
        df: 数据框
        selected_modules: 选中的模块列表
        selected_statuses: 选中的状态列表
    """
    # 应用状态映射
    df = apply_status_mapping(df)
    
    # 如果指定了模块过滤
    if selected_modules and '缺陷模块' in df.columns:
        # 检查是否选中了"（空）"选项
        if '（空）' in selected_modules:
            # 移除"（空）"选项，单独处理
            selected_modules_copy = [m for m in selected_modules if m != '（空）']
            # 筛选：模块在选中列表中 或 模块为空
            if selected_modules_copy:
                df = df[df['缺陷模块'].isin(selected_modules_copy) | df['缺陷模块'].isna()]
            else:
                # 只选中了"（空）"
                df = df[df['缺陷模块'].isna()]
        else:
            # 没有选中"（空）"，按正常逻辑过滤
            df = df[df['缺陷模块'].isin(selected_modules)]
    
    # 如果指定了状态过滤
    # selected_statuses 是映射后的状态（如"待修复"），需要转换为原始状态进行筛选
    if selected_statuses:
        # 创建反向映射：从映射后的状态找到所有对应的原始状态
        reverse_mapping = {}
        for original_status, mapped_status in STATUS_MAPPING.items():
            if mapped_status not in reverse_mapping:
                reverse_mapping[mapped_status] = []
            reverse_mapping[mapped_status].append(original_status)
        
        # 将映射后的状态转换为原始状态列表
        original_statuses = []
        status_col = '原始状态' if '原始状态' in df.columns else '状态'
        
        if status_col in df.columns:
            # 获取所有原始状态
            all_original_statuses = df[status_col].dropna().unique().tolist()
            
            for mapped_status in selected_statuses:
                if mapped_status in reverse_mapping:
                    # 找到映射到这个状态的所有原始状态
                    original_statuses.extend(reverse_mapping[mapped_status])
                else:
                    # 如果不在映射表中，说明本身就是原始状态（如"已关闭"、"已解决"等）
                    if mapped_status in all_original_statuses:
                        original_statuses.append(mapped_status)
            
            # 去重并筛选
            if original_statuses:
                original_statuses = list(set(original_statuses))
                df = df[df[status_col].isin(original_statuses)]
    
    stats = {}
    current_date = datetime.now()
    
    # 1. 不同状态下，统计缺陷数量【count(标题)】
    # 使用映射后状态，将新建、修复中、待修复合并显示为"待修复"
    if '映射后状态' in df.columns and '标题' in df.columns:
        status_count = df.groupby('映射后状态')['标题'].count().to_dict()
        stats['status_count'] = status_count
    elif '状态' in df.columns and '标题' in df.columns:
        status_count = df.groupby('状态')['标题'].count().to_dict()
        stats['status_count'] = status_count
    else:
        stats['status_count'] = {}
    
    # 2. 缺陷停留时长
    # 统计状态为待修复的缺陷（新建、修复中、待修复等已映射为待修复）
    # 停留时长 = 当前时间所在天 - 创建时间所在天（单位：天）
    if '映射后状态' in df.columns and '创建时间' in df.columns and '标题' in df.columns:
        # 筛选映射后状态为'待修复'的缺陷（包括原始的新建、修复中等）
        pending_defects = df[df['映射后状态'] == '待修复'].copy()
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
                # 转换为字符串键，方便JSON序列化
                stats['stay_duration'] = {str(int(k)): int(v) for k, v in sorted(stay_duration.items())}
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
        # 按创建日期分组统计缺陷数量，过滤掉空日期
        df_copy = df_copy[df_copy['创建日期'].notna()]
        if len(df_copy) > 0:
            daily_new = df_copy.groupby('创建日期')['标题'].count().to_dict()
            # 按日期排序并格式化
            daily_stats['daily_new'] = {k.strftime('%Y-%m-%d'): int(v) for k, v in sorted(daily_new.items())}
        else:
            daily_stats['daily_new'] = {}
    else:
        daily_stats['daily_new'] = {}
    
    # 每日修复：待验证状态且更新时间为对应天 + 已关闭状态且完成时间为对应天
    # 使用原始状态列进行统计
    daily_fixed = {}
    
    # 1) 待验证状态的缺陷，使用更新时间
    status_col = '原始状态' if '原始状态' in df.columns else '状态'
    if status_col in df.columns and '更新时间' in df.columns and '标题' in df.columns:
        pending_verify = df[df[status_col] == '待验证'].copy()
        if len(pending_verify) > 0:
            # 将更新时间转换为日期
            pending_verify['更新日期'] = pd.to_datetime(pending_verify['更新时间'], errors='coerce').dt.date
            # 过滤掉空日期
            pending_verify = pending_verify[pending_verify['更新日期'].notna()]
            if len(pending_verify) > 0:
                # 按更新日期统计
                for date, count in pending_verify.groupby('更新日期')['标题'].count().items():
                    date_str = date.strftime('%Y-%m-%d')
                    daily_fixed[date_str] = daily_fixed.get(date_str, 0) + int(count)
    
    # 2) 已关闭状态的缺陷，使用完成时间
    if status_col in df.columns and '完成时间' in df.columns and '标题' in df.columns:
        closed = df[df[status_col] == '已关闭'].copy()
        if len(closed) > 0:
            # 将完成时间转换为日期
            closed['完成日期'] = pd.to_datetime(closed['完成时间'], errors='coerce').dt.date
            # 过滤掉空日期
            closed = closed[closed['完成日期'].notna()]
            if len(closed) > 0:
                # 按完成日期统计
                for date, count in closed.groupby('完成日期')['标题'].count().items():
                    date_str = date.strftime('%Y-%m-%d')
                    daily_fixed[date_str] = daily_fixed.get(date_str, 0) + int(count)
    
    # 按日期排序
    daily_stats['daily_fixed'] = {k: v for k, v in sorted(daily_fixed.items())}
    stats['daily_stats'] = daily_stats
    
    # 4. 缺陷分析归类统计（饼图）
    if classification_mode == 'keyword' and keywords and '标题' in df.columns:
        # 关键字匹配归类模式
        df_analysis = df.copy()
        df_analysis['分析类型_显示'] = '其他'  # 默认归类为"其他"
        
        # 对每个关键字进行模糊匹配
        for keyword in keywords:
            if keyword and keyword.strip():  # 确保关键字不为空
                keyword = keyword.strip()
                # 使用str.contains进行模糊匹配（不区分大小写）
                mask = df_analysis['标题'].astype(str).str.contains(keyword, case=False, na=False, regex=False)
                df_analysis.loc[mask, '分析类型_显示'] = keyword
        
        analysis_count = df_analysis.groupby('分析类型_显示')['标题'].count().to_dict()
        stats['analysis_type_count'] = analysis_count
    else:
        # 人工归类模式（原有功能）
        # 支持多种列名：缺陷分析类型、缺陷分析归类、缺陷分类
        analysis_col = None
        for col_name in ['缺陷分析类型', '缺陷分析归类', '缺陷分类']:
            if col_name in df.columns:
                analysis_col = col_name
                break
        
        if analysis_col and '标题' in df.columns:
            df_analysis = df.copy()
            # 将空值替换为"（空）"，以便在图表中显示
            df_analysis['分析类型_显示'] = df_analysis[analysis_col].fillna('（空）')
            analysis_count = df_analysis.groupby('分析类型_显示')['标题'].count().to_dict()
            stats['analysis_type_count'] = analysis_count
        else:
            stats['analysis_type_count'] = {}
    
    return stats

def get_module_list(df):
    """
    获取缺陷模块列表（去重），包含空值选项
    """
    if '缺陷模块' in df.columns:
        # 获取非空模块
        modules = df['缺陷模块'].dropna().unique().tolist()
        modules = sorted(modules)
        
        # 检查是否有空模块，如果有则添加"（空）"选项
        has_empty = df['缺陷模块'].isna().any()
        if has_empty:
            modules.insert(0, '（空）')  # 在列表开头添加空选项
        
        return modules
    return []

def get_status_list(df):
    """
    获取状态列表（去重），返回映射后的状态
    新建、修复中、待修复等会合并显示为"待修复"
    """
    # 复制数据框避免修改原始数据
    df_copy = df.copy()
    # 先应用状态映射
    df_copy = apply_status_mapping(df_copy)
    
    # 使用映射后的状态列
    if '映射后状态' in df_copy.columns:
        # 获取非空状态（映射后的）
        statuses = df_copy['映射后状态'].dropna().unique().tolist()
        statuses = sorted(statuses)
        return statuses
    elif '状态' in df_copy.columns:
        # 如果没有映射后状态，使用原始状态
        statuses = df_copy['状态'].dropna().unique().tolist()
        statuses = sorted(statuses)
        return statuses
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
        
        # 获取模块列表和状态列表
        modules = get_module_list(df)
        statuses = get_status_list(df)
        
        # 存储数据（使用timestamp作为key）
        uploaded_data[timestamp] = {
            'filepath': filepath,
            'dataframe': df,
            'modules': modules,
            'statuses': statuses
        }
        
        return jsonify({
            'success': True,
            'timestamp': timestamp,
            'modules': modules,
            'statuses': statuses,
            'total_records': len(df)
        })
        
    except Exception as e:
        return jsonify({'error': f'处理文件时出错: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze_data():
    """根据选择的模块和状态分析数据并返回图表数据"""
    try:
        data = request.json
        timestamp = data.get('timestamp')
        selected_modules = data.get('modules', [])
        selected_statuses = data.get('statuses', [])
        
        if not timestamp or timestamp not in uploaded_data:
            return jsonify({'error': '数据不存在或已过期'}), 400
        
        # 获取存储的数据
        df = uploaded_data[timestamp]['dataframe'].copy()
        
        # 如果没有选择模块，使用全部模块
        if not selected_modules:
            selected_modules = uploaded_data[timestamp]['modules']
        
        # 如果没有选择状态，使用全部状态
        if not selected_statuses:
            selected_statuses = uploaded_data[timestamp].get('statuses', [])
        
        # 获取归类方式和关键字
        classification_mode = data.get('classification_mode', 'manual')
        keywords = data.get('keywords', [])
        
        # 生成统计数据
        stats = analyze_defect_data(df, selected_modules, selected_statuses, classification_mode, keywords)
        
        # 转换为JSON可序列化的格式
        result = {
            'success': True,
            'stats': stats,
            'selected_modules': selected_modules,
            'selected_statuses': selected_statuses,
            'filtered_records': len(df)
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'分析数据时出错: {str(e)}'}), 500

# 关键字文件路径
KEYWORDS_FILE = 'keywords.json'

def load_keywords():
    """从文件加载关键字列表"""
    if os.path.exists(KEYWORDS_FILE):
        try:
            with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('keywords', [])
        except:
            return []
    return []

def save_keywords(keywords):
    """保存关键字列表到文件"""
    try:
        with open(KEYWORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump({'keywords': keywords}, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        return False

@app.route('/api/keywords', methods=['GET'])
def get_keywords():
    """获取关键字列表"""
    keywords = load_keywords()
    return jsonify({'success': True, 'keywords': keywords})

@app.route('/api/keywords', methods=['POST'])
def add_keyword():
    """添加关键字"""
    try:
        data = request.json
        keyword = data.get('keyword', '').strip()
        
        if not keyword:
            return jsonify({'error': '关键字不能为空'}), 400
        
        keywords = load_keywords()
        if keyword not in keywords:
            keywords.append(keyword)
            if save_keywords(keywords):
                return jsonify({'success': True, 'keywords': keywords})
            else:
                return jsonify({'error': '保存关键字失败'}), 500
        else:
            return jsonify({'error': '关键字已存在'}), 400
    except Exception as e:
        return jsonify({'error': f'添加关键字失败: {str(e)}'}), 500

@app.route('/api/keywords', methods=['DELETE'])
def delete_keyword():
    """删除关键字"""
    try:
        data = request.json
        keyword = data.get('keyword', '').strip()
        
        if not keyword:
            return jsonify({'error': '关键字不能为空'}), 400
        
        keywords = load_keywords()
        if keyword in keywords:
            keywords.remove(keyword)
            if save_keywords(keywords):
                return jsonify({'success': True, 'keywords': keywords})
            else:
                return jsonify({'error': '保存关键字失败'}), 500
        else:
            return jsonify({'error': '关键字不存在'}), 400
    except Exception as e:
        return jsonify({'error': f'删除关键字失败: {str(e)}'}), 500

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

