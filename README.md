
# 🔓 JIF-VLM: Jailbreaking Multimodal Language Models via Multi-Level Noise

![JIF-VLM Overview](https://github.com/user-attachments/assets/7379c2b5-e733-4dc5-93dd-24f628bdf41d)
## 🧠 Overview

**JIF-VLM** introduces a novel and robust approach to jailbreaking **Multimodal Large Language Models (MLLMs)** for text-to-image generation. Inspired by FigStep and best-of-n sampling strategies, our method applies **multi-level noise transformations**—semantic, syntactic, and image-level—to bypass safety filters while preserving semantic intent.

Unlike prior work that focuses on hiding prompts, JIF-VLM actively **manipulates and perturbs input text** to generate adversarial prompts without relying on external LLMs. This significantly reduces computational overhead while maintaining high attack success rates across multiple state-of-the-art MLLMs.

---

## 🚀 Key Features

- **Multi-Level Noise Pipeline**  
  Introduces controlled perturbations at:
  - **Semantic level** (e.g., synonym substitution)
  - **Syntactic level** (e.g., structure reordering)
  - **Image level** (e.g., pixel-space transformations)

- **LLM-Free Prompt Generation**  
  Eliminates the need for external LLMs to generate adversarial prompts, improving efficiency and reproducibility.

- **Extensive Evaluation**  
  Tested on the **SafeBench-Tiny** dataset with over **5,600 generated images**, demonstrating strong jailbreak performance across multiple MLLMs including **LLaVa** and **IBM Granite**.

- **Plug-and-Play Design**  
  Easily integrates with existing MLLM pipelines and supports batch testing and benchmarking.

---

## 🧪 Technologies Used

- Python, PyTorch, Transformers  
- BERT, LLaVa, IBM Granite  
- FastAPI (for web interface)  
- SafeBench-Tiny dataset

---

## 📂 Repository

[🔗 GitHub: rndae/jif-vlm-jailbreak](https://github.com/rndae/jif-vlm-jailbreak)
