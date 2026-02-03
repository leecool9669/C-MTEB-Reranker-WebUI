# -*- coding: utf-8 -*-
"""BGE-Reranker-Large 重排序 WebUI 演示（不加载真实模型权重）。"""
from __future__ import annotations

import gradio as gr


def fake_load_model():
    """模拟加载模型，实际不下载权重，仅用于界面演示。"""
    return "模型状态：BGE-Reranker-Large 已就绪（演示模式，未加载真实权重）"


def fake_rerank(query: str, passages: str, top_k: int) -> str:
    """模拟对查询与候选文档进行重排序并返回可视化结果。"""
    query = (query or "").strip()
    passages = (passages or "").strip()
    if not query:
        return "请输入查询文本。"
    lines = [f"查询：{query}", ""]
    if not passages:
        lines.append("未输入候选文档，请每行填写一条候选文档后再执行重排序。")
        return "\n".join(lines)
    doc_list = [p.strip() for p in passages.split("\n") if p.strip()]
    if not doc_list:
        lines.append("未解析到有效候选文档，请每行填写一条。")
        return "\n".join(lines)
    k = max(1, min(len(doc_list), int(top_k) if isinstance(top_k, (int, float)) else 5))
    lines.append("[演示] 已对查询与候选文档进行重排序（未加载真实模型）。")
    lines.append(f"Top-{k} 结果示例（分数为占位）：")
    for i, doc in enumerate(doc_list[:k], 1):
        score = 0.95 - (i - 1) * 0.05
        lines.append(f"  {i}. 分数: {score:.4f} — {doc[:50]}{'...' if len(doc) > 50 else ''}")
    lines.append("\n加载真实 BGE-Reranker-Large 后，将在此显示实际相关性分数与排序。")
    return "\n".join(lines)


def build_ui():
    with gr.Blocks(title="BGE-Reranker-Large WebUI") as demo:
        gr.Markdown("## BGE-Reranker-Large 重排序 · WebUI 演示")
        gr.Markdown(
            "本界面以交互方式展示 BGE-Reranker-Large 跨编码器重排序模型的典型使用流程，"
            "包括模型加载状态与「查询—文档」相关性打分与排序结果展示。"
        )

        with gr.Row():
            load_btn = gr.Button("加载模型（演示）", variant="primary")
            status_box = gr.Textbox(label="模型状态", value="尚未加载", interactive=False)
        load_btn.click(fn=fake_load_model, outputs=status_box)

        with gr.Tabs():
            with gr.Tab("重排序"):
                gr.Markdown("在下方输入查询与若干候选文档（每行一条），模型将输出相关性分数及排序结果。")
                query_in = gr.Textbox(
                    label="查询",
                    placeholder="例如：什么是大熊猫？",
                    lines=2,
                )
                passages_in = gr.Textbox(
                    label="候选文档（每行一条）",
                    placeholder="文档1\n文档2\n...",
                    lines=8,
                )
                top_k = gr.Slider(
                    minimum=1, maximum=20, value=5, step=1, label="展示 Top-K 条"
                )
                out = gr.Textbox(label="重排序结果", lines=12, interactive=False)
                run_btn = gr.Button("执行重排序（演示）")
                run_btn.click(
                    fn=fake_rerank,
                    inputs=[query_in, passages_in, top_k],
                    outputs=out,
                )

        gr.Markdown(
            "---\n*说明：当前为轻量级演示界面，未实际下载与加载 BGE-Reranker-Large 模型参数。*"
        )

    return demo


def main():
    app = build_ui()
    app.launch(server_name="127.0.0.1", server_port=8761, share=False)


if __name__ == "__main__":
    main()
