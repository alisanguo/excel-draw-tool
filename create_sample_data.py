"""
创建示例缺陷数据Excel文件
"""
import pandas as pd
from datetime import datetime, timedelta
import random

# 设置中文字体支持
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 准备示例数据
status_list = ['待解决', '处理中', '已解决', '已关闭', '重新打开']
category_list = ['功能缺陷', '性能问题', '界面问题', '兼容性问题', '安全问题']
level_list = ['A', 'B', 'C', 'D']  # 缺陷级别
tag_list = ['【二阶段】', '【三阶段】', '【紧急】', '【常规】']  # 标签
module_list = ['用户模块', '订单模块', '支付模块', '商品模块', '系统设置']
handler_list = ['张三', '李四', '王五', '赵六', '钱七']
reason_list = ['需求理解偏差', '代码逻辑错误', '测试不充分', '环境配置问题', '第三方接口问题']

# 生成50条示例数据
num_records = 50
data = []

base_date = datetime(2020, 1, 1)

for i in range(num_records):
    record_id = f"55{600 + i:03d}"
    status = random.choice(status_list)
    tag = random.choice(tag_list)
    title = f"{tag}{random.choice(['用户无法登录', '数据显示错误', '页面加载缓慢', '按钮点击无响应', '数据保存失败'])}"
    category = random.choice(category_list)
    level = random.choice(level_list)
    module = random.choice(module_list)
    handler = random.choice(handler_list)
    reason = random.choice(reason_list)
    
    # 生成时间
    create_days = random.randint(0, 365)
    create_time = base_date + timedelta(days=create_days, hours=random.randint(8, 18), minutes=random.randint(0, 59))
    update_time = create_time + timedelta(hours=random.randint(1, 72))
    
    # 如果已解决或已关闭，添加完成时间
    complete_time = None
    if status in ['已解决', '已关闭']:
        complete_time = update_time + timedelta(hours=random.randint(1, 48))
    
    data.append({
        '事项ID': record_id,
        '事项类型': '缺陷',
        '标签': tag,
        '标题': title,
        '状态': status,
        '创建时间': create_time.strftime('%Y-%m-%d %H:%M:%S'),
        '更新时间': update_time.strftime('%Y-%m-%d %H:%M:%S'),
        '完成时间': complete_time.strftime('%Y-%m-%d %H:%M:%S') if complete_time else '',
        '处理人': handler,
        '责任原因': reason,
        '缺陷分类': category,
        '缺陷级别': level,
        '缺陷模块': module,
        '缺陷分析类型': random.choice(['A类', 'B类', 'C类'])
    })

# 创建DataFrame
df = pd.DataFrame(data)

# 保存到Excel
output_file = 'sample_defect_data.xlsx'
df.to_excel(output_file, index=False, sheet_name='缺陷数据')

print(f"示例数据已生成：{output_file}")
print(f"共生成 {len(df)} 条缺陷记录")
print("\n数据预览：")
print(df.head(10))

