// static/script.js - 更新版 (配合Spinner和Fade-in效果)

// 等待HTML文档完全加载并解析完成后再执行脚本
document.addEventListener('DOMContentLoaded', (event) => {

    // 获取页面上的重要元素
    const submitButton = document.getElementById('submitBtn');
    const userInputElement = document.getElementById('userInput');
    const resultsDiv = document.getElementById('results');
    const loadingSpinner = document.getElementById('loadingSpinner'); // 新增：获取加载动画元素

    // 检查元素是否存在
    if (!submitButton || !userInputElement || !resultsDiv || !loadingSpinner) {
        console.error("页面缺少必要的元素：submitBtn, userInput, results, 或 loadingSpinner。");
        // 如果缺少元素，也尝试给用户一个提示
        if (resultsDiv) {
            resultsDiv.innerHTML = '<p style="color: var(--error-color);">页面加载不完整，请联系管理员。</p>';
            resultsDiv.style.display = 'block';
        }
        return;
    }

    // 为提交按钮添加点击事件监听器
    submitButton.addEventListener('click', async () => {
        // 1. 获取用户输入
        const userInput = userInputElement.value.trim();

        // 2. 前端验证
        if (!userInput) {
            resultsDiv.innerHTML = '<p style="color: var(--error-color);">请输入内容后再提交！</p>'; // 使用innerHTML设置错误信息样式
            resultsDiv.classList.remove('visible'); // 确保移除可能残留的visible类
            resultsDiv.style.display = 'block'; // 显示错误信息
            loadingSpinner.style.display = 'none'; // 确保加载动画隐藏
            userInputElement.focus();
            return;
        }

        // 3. 准备开始处理：重置状态、显示加载动画
        resultsDiv.classList.remove('visible'); // **新增**: 移除 visible 类，重置透明度为0
        resultsDiv.innerHTML = '';             // 清空旧结果或错误信息
        resultsDiv.style.display = 'none';      // **修改**: 先隐藏结果区域
        loadingSpinner.style.display = 'block'; // **新增**: 显示加载动画
        submitButton.disabled = true;           // 禁用按钮

        try {
            // 4. 发送请求到后端
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ userInput: userInput }),
            });

            // 5. 处理后端响应
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: `服务器错误，状态码: ${response.status}` }));
                throw new Error(errorData.error || `HTTP 错误! 状态码: ${response.status}`);
            }

            const data = await response.json();

            // 6. 显示结果 (成功时)
            if (data.result) {
                 // 假设您仍想渲染Markdown，使用marked.js
                 // 如果您完全依赖Prompt优化，不需要Markdown渲染，请替换成下一行注释掉的代码
                resultsDiv.innerHTML = marked.parse(data.result);
                // resultsDiv.textContent = data.result; // 如果不需要Markdown渲染，用这行
            } else {
                resultsDiv.textContent = '未能获取到有效结果。';
            }
             // **修改**: 使用 requestAnimationFrame 添加 visible 类以触发淡入
             requestAnimationFrame(() => {
                 resultsDiv.style.display = 'block'; // 先确保div是block状态
                 requestAnimationFrame(() => { // 再添加类，确保浏览器有时间应用display:block
                     resultsDiv.classList.add('visible');
                 });
             });


        } catch (error) {
            // 7. 显示错误信息 (出错时)
            console.error('请求处理失败:', error);
            resultsDiv.innerHTML = `<p style="color: var(--error-color); margin:0;">处理失败: ${error.message}</p>`; // 使用innerHTML设置错误信息样式, 去掉默认margin
            // **修改**: 同样使用 requestAnimationFrame 添加 visible 类
             requestAnimationFrame(() => {
                 resultsDiv.style.display = 'block';
                 requestAnimationFrame(() => {
                     resultsDiv.classList.add('visible');
                 });
             });

        } finally {
            // 8. 无论成功失败，隐藏加载动画并启用按钮
            loadingSpinner.style.display = 'none'; // **新增**: 隐藏加载动画
            // 注意：结果区的display已经在try或catch中设置为block了
            submitButton.disabled = false;         // 启用按钮
        }
    });

}); // DOMContentLoaded 事件监听结束