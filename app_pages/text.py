import streamlit as st

import asyncio
from utils import api
from utils.hf_helper import hf_api, get_models_list
from utils.hf_inference import (
    get_inference,
    get_inference_from_gradio_client,
    get_serverless_models_list,
)

# Variables
tasks = [
    "sentiment-analysis",
    "text-classification",
    "summarization",
    "question-answering",
    "translation",
    "text-generation",
    "Maths Solver",
    "Code-Generation",
]

# region:Display Elements commun elements
with st.sidebar:
    task = st.selectbox("Choose Tasks", tasks, on_change=api.get_API_URL.cache_clear())


with st.popover("Explore Models", use_container_width=True):
    col1, col2 = st.columns([1, 3])
    key_sort = col1.radio("Sortby", ["downloads", "likes", "last_modified", "trending"])
    lang = col1.multiselect(
        "Language", ["en", "fr", "ar", "es", "de", "jp"], default=["en"]
    )
    limit = col1.slider("Limit to", min_value=5, max_value=20, value=5, step=5)
    models_list = get_models_list(task, key_sort, language=lang)[:limit]
    col2.dataframe(models_list, use_container_width=False)


with st.sidebar:
    selected_model = st.selectbox(
        "Choose Model",
        [model["id"] for model in models_list],
        key="select_model",
        on_change=api.get_API_URL.cache_clear(),
    )
if selected_model is not None:
    model_info = hf_api.model_info(selected_model)
    st.popover("Model Info").write(model_info.cardData)
# endregion:Display Elements commun elements
with st.form(f"{task}"):
    input_text = st.text_area(f"{task.upper()}")
    col_params, col_submit = st.columns([4, 1], gap="small")
    task = "text-classification" if task == "sentiment-analysis" else task
    if task == "summarization":
        text_length = len(input_text.split()) if input_text else 0
        if text_length < 10:
            st.warning("Text is too short to be summarized")
        else:
            with col_params.popover(
                "Summarization Parameters",
                use_container_width=True,
                help="Try different parameters to get better results",
            ):
                to_clean_up_spaces = st.checkbox("Clean Up Spaces", value=True)
                max_length = st.slider(
                    "Max Length",
                    min_value=30,
                    max_value=int(0.9 * text_length),
                    value=int(0.5 * text_length),
                )
    elif task == "question-answering":
        question_text = col_params.text_input("Put your question here")
    if col_submit.form_submit_button("Submit", use_container_width=True):
        match task:
            case "text-classification":
                inputs = {"inputs": input_text}
                try:
                    # outputs = asyncio.run(api.query_text(inputs, model_id=selected_model))
                    outputs = asyncio.run(
                        get_inference(input_text, selected_model, task=task)
                    )
                    # st.json(outputs)
                    label = outputs[0].label.upper()
                    score = outputs[0].score
                    # display
                    col_label, col_score, col_rest = st.columns([2, 1, 3], gap="small")
                    col_label.success(label)
                    col_score.metric("Score", value=f"{score:.2%}")
                    with col_rest.popover(
                        "Show all posibilities", use_container_width=True
                    ):
                        for output in outputs:
                            col_label, col_score = st.columns([2, 1], gap="small")
                            col_label.progress(output.score, text=output.label.upper())
                            col_score.write(f"{output.score:.1%}")
                except Exception as e:
                    st.exception("Choose another model")
            case "summarization":
                # prediction
                inputs = input_text
                parameters = {
                    "max_length": max_length,
                    "clean_up_tokenization_spaces": to_clean_up_spaces,
                }
                # outputs = asyncio.run(api.query_text(inputs, model_id=selected_model))
                outputs = asyncio.run(
                    get_inference(inputs, selected_model, task, parameters=parameters)
                )
                st.json(outputs)
                try:
                    summary_text = (
                        "No summary inferred"
                        if outputs["summary_text"] is None
                        else outputs["summary_text"]
                    )
                except:
                    summary_text = outputs["translation_text"]
                # display
                st.text_area("Summarized Text: ", value=summary_text)
                st.success(
                    f"Summary Percentage: {len(summary_text.split()) / text_length:.0%}"
                )
                # st.write(pipeline_model.model.config.min_length)
            case "translation":
                # prediction
                inputs = input_text
                parameters = {
                    "src_lang": "en",
                    "tgt_lang": "fr",
                }
                # outputs = asyncio.run(api.query_text(inputs, model_id=selected_model))
                outputs = asyncio.run(
                    get_inference(inputs, selected_model, task, parameters=parameters)
                )
                # st.json(outputs)
                translated_text = outputs["translation_text"]
                # display
                st.text_area("Translation:", value=translated_text)
            case "question-answering":
                # prediction
                if len(question_text) > 2:
                    inputs = {"question": question_text, "context": input_text}
                    # output = asyncio.run(api.query_text(inputs))
                    outputs = asyncio.run(get_inference(inputs, selected_model, task))
                    # st.json(outputs)
                    answer = outputs["answer"]
                    score = outputs["score"]
                    # display
                    col1, col2 = st.columns(2, gap="small")
                    col1.success(answer)
                    col2.metric("Score", value=f"{score:.2%}")

            case "Code-Generation":
                inputs = input_text
                outputs = get_inference_from_gradio_client(
                    inputs, model_id="Tonic/Yi-Coder-9B"
                )
                st.code(outputs)
            case "Maths Solver":
                st.subheader("Maths Solver")
                # Use a pipeline as a high-level helper
                # from transformers import pipeline
                # pipe = pipeline("text-generation", model="AI-MO/NuminaMath-7B-TIR", torch_dtype=torch.bfloat16, device_map="auto")
                # messages = [
                #     {"role": "user", "content": "For how many values of the constant $k$ will the polynomial $x^{2}+kx+36$ have two distinct integer roots?"},
                # ]
                # prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                # gen_config = {
                #     "max_new_tokens": 1024,
                #     "do_sample": False,
                #     "stop_strings": ["```output"], # Generate until Python code block is complete
                #     "tokenizer": pipe.tokenizer,
                # }
                # outputs = pipe(prompt, **gen_config)
                # text = outputs[0]["generated_text"]
                # st.write(text)
                st.link_button(
                    "Open maths solver",
                    url="https://huggingface.co/spaces/AI-MO/math-olympiad-solver",
                )  # https://huggingface.co/spaces/AI-MO/math-olympiad-solver
                st.page_link(
                    label="Open maths solver",
                    page="https://huggingface.co/spaces/AI-MO/math-olympiad-solver",
                )
                st.html(
                    """
                        <iframe src="https://huggingface.co/spaces/AI-MO/math-olympiad-solver" width="100%" height="500"</iframe>
                        """
                )
            case _:
                st.warning("Not implimented")

st.write(asyncio.run(
    get_serverless_models_list(task)))
# import torch
# st.write(torch.cuda.is_available())
# st.write(tf.test.is_gpu_available(cuda_only=True))
