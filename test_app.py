"""
简单测试脚本，验证统计功能是否正常
"""
import pandas as pd
from app import analyze_defect_data, get_module_list, apply_status_mapping

def test_analyze():
    print("=" * 60)
    print("测试缺陷数据分析功能")
    print("=" * 60)
    
    # 读取示例数据
    try:
        df = pd.read_excel('sample_defect_data.xlsx')
        print(f"\n✓ 成功读取示例数据，共 {len(df)} 条记录")
        print(f"✓ 列名: {list(df.columns)}")
    except Exception as e:
        print(f"\n✗ 读取数据失败: {e}")
        return
    
    # 测试模块列表提取
    print("\n" + "-" * 60)
    print("测试模块列表提取")
    print("-" * 60)
    modules = get_module_list(df)
    print(f"✓ 提取到 {len(modules)} 个模块: {modules}")
    
    # 测试状态映射
    print("\n" + "-" * 60)
    print("测试状态映射")
    print("-" * 60)
    df_mapped = apply_status_mapping(df.copy())
    print("✓ 状态映射前后对比:")
    if '原始状态' in df_mapped.columns:
        status_mapping = df_mapped[['原始状态', '状态']].drop_duplicates()
        print(status_mapping.to_string(index=False))
    
    # 测试数据分析
    print("\n" + "-" * 60)
    print("测试数据分析（全部模块）")
    print("-" * 60)
    
    try:
        stats = analyze_defect_data(df.copy())
        
        # 1. 状态统计
        if 'status_count' in stats:
            print(f"\n1. 不同状态下的缺陷数量:")
            for status, count in stats['status_count'].items():
                print(f"   - {status}: {count}")
        
        # 2. 停留时长
        if 'stay_duration' in stats:
            print(f"\n2. 缺陷停留时长（待修复状态）:")
            if stats['stay_duration']:
                for days, count in sorted(stats['stay_duration'].items(), key=lambda x: int(x[0])):
                    print(f"   - {days}天: {count}个")
            else:
                print("   （无待修复状态的缺陷）")
        
        # 3. 每日新增/修复
        if 'daily_stats' in stats:
            print(f"\n3. 每日新增/修复统计:")
            daily_new = stats['daily_stats'].get('daily_new', {})
            daily_fixed = stats['daily_stats'].get('daily_fixed', {})
            print(f"   - 每日新增数据点: {len(daily_new)}")
            print(f"   - 每日修复数据点: {len(daily_fixed)}")
            if daily_new:
                print(f"   - 新增数据示例 (前3条):")
                for i, (date, count) in enumerate(list(daily_new.items())[:3]):
                    print(f"     {date}: {count}个")
        
        # 4. 分析类型
        if 'analysis_type_count' in stats:
            print(f"\n4. 缺陷分析类型统计:")
            for type_name, count in stats['analysis_type_count'].items():
                print(f"   - {type_name}: {count}")
        
        print(f"\n✓ 数据分析完成!")
        
    except Exception as e:
        print(f"\n✗ 数据分析失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试模块过滤
    print("\n" + "-" * 60)
    print("测试模块过滤（选择前2个模块）")
    print("-" * 60)
    
    if modules:
        selected_modules = modules[:2]
        print(f"✓ 选择模块: {selected_modules}")
        
        try:
            stats_filtered = analyze_defect_data(df.copy(), selected_modules)
            
            if 'status_count' in stats_filtered:
                total = sum(stats_filtered['status_count'].values())
                print(f"✓ 过滤后的总记录数: {total}")
                print(f"✓ 状态分布: {stats_filtered['status_count']}")
            
        except Exception as e:
            print(f"✗ 模块过滤失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)

if __name__ == '__main__':
    test_analyze()

