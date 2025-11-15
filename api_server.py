from flask import Flask, request, jsonify
import asyncio
import subprocess
import sys
import os
import json
from tools.time_util import get_current_date
# 获取目录中所有文件
import os
import glob

def find_latest_files(directory, pattern):
    """查找目录中匹配模式的最新文件"""
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return None
    # 按修改时间排序，返回最新的文件
    return max(files, key=os.path.getmtime)


def read_json_data_with_limit(file_path):
    """
    读取JSON文件数据并返回前N条记录
    
    Args:
        file_path (str): JSON文件路径
        limit (int): 返回的最大记录数，默认为5
        
    Returns:
        list: 包含前N条记录的列表，如果文件不存在或读取失败返回空列表
    """
    # 读取内容数据（前5条）
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
            return all_data[:5]
    

app = Flask(__name__)
@app.route('/crawl', methods=['POST'])
def crawl():
    try:
        data = request.json
        platform = data.get('platform', 'xhs')
        cookies = data.get('cookies', '')
        keywords = data.get('keywords', '')
        sort_type = data.get('sort_type', '')
        filter_note_type = data.get('filter_note_type', '')
        filter_note_time = data.get('filter_note_time', '')
        max_notes_count = data.get('max_notes_count', '')
        max_comments_count_single = data.get('max_comments_count_single_note', '')
        
        # 执行爬虫命令，但不在API响应中返回控制台输出
        cmd = [sys.executable, 'main.py', '--platform', platform, '--type', 'search']
        
        # 如果提供了cookies，则使用cookie登录方式
        if cookies:
            cmd.extend(['--lt', 'cookie', '--cookies', cookies])
            
        # 如果提供了keywords，则添加关键词参数
        if keywords:
            cmd.extend(['--keywords', keywords])
        if max_notes_count:
            cmd.extend(['--max_notes_count', str(max_notes_count)])
        if max_comments_count_single:
            cmd.extend(['--max_comments_count_single_note', str(max_comments_count_single)])
            
        # 只有小红书平台支持动态过滤器参数，直接通过CLI传递
        if platform == "xhs":
            if sort_type:
                cmd.extend(["--sort_type", str(sort_type)])
            if filter_note_type:
                cmd.extend(["--filter_note_type", str(filter_note_type)])
            if filter_note_time:
                cmd.extend(["--filter_note_time", str(filter_note_time)])
        else:
            if sort_type or filter_note_type or filter_note_time:
                print(f"警告: 平台 {platform} 不支持过滤器参数，参数将被忽略")
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=os.getcwd(),
            timeout=600  # 10分钟超时
        )
        
        # 在终端显示控制台输出（但不在API响应中返回）
        print("=== 爬虫执行输出 ===")
        print("返回码:", result.returncode)
        if result.stdout:
            print("标准输出:", result.stdout)
        if result.stderr:
            print("错误输出:", result.stderr)
        print("===================")
        
        if result.returncode != 0:
            return jsonify({
                "status": "error",
                "message": "爬虫执行失败",
                "error_code": result.returncode
            }), 500
        
        # 读取生成的JSON文件并返回前5条数据
        # 查找目录中最新的文件，避免跨进程变量不一致问题
        json_dir = f"data/{platform}/json"
        

        # 查找最新的内容文件和评论文件
        contents_file = find_latest_files(json_dir, "search_contents_*.json")
        comments_file = find_latest_files(json_dir, "search_comments_*.json")
        
        # 检查文件是否存在
        if not contents_file or not os.path.exists(contents_file):
            return jsonify({
                "status": "error",
                "message": "未找到内容数据文件，请确保爬虫已成功执行"
            }), 404
        
        if not comments_file or not os.path.exists(comments_file):
            return jsonify({
                "status": "error", 
                "message": "未找到评论数据文件，请确保爬虫已成功执行"
            }), 404
        
        result_data = {"contents": [], "comments": []}
        
        # 使用工具函数读取内容数据（前5条）
        contents = read_json_data_with_limit(contents_file)
        
        # 使用工具函数读取评论数据（前5条）
        comments = read_json_data_with_limit(comments_file)
        
        return jsonify({
            "status": "success",
            "platform": platform,
            "data": {
                "contents": contents,
                "comments": comments
            }
        })
            
    except subprocess.TimeoutExpired:
        return jsonify({
            "status": "timeout",
            "message": "爬虫执行超时（超过10分钟）"
        }), 504
    except Exception as e:
        print("API错误:", str(e))
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5101, debug=True)
