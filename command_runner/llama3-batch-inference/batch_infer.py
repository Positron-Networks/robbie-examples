import argparse
import pandas as pd
from tqdm import tqdm
from vllm import LLM, SamplingParams
"""Batch Inference - Use Llama3 to determine the topic and sentiment of a chat conversation transcript"""

MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"
USER_DATA_CSV = "dialogueText_301_cleaned_v2.csv"

# Prompt credit to EndeavorCX - https://developers.endeavorcx.com/docs/topic-level-sentiment-analysis
SYSTEM_PROMPT = """
You are a highly experienced Customer Experience (CX) sentiment analysis expert with extensive training in handling timestamped transcripts of conversations. Your task is to identify key topics from a provided timestamped transcript and analyze their sentiment over time. You must follow all instructions carefully.

Objectives & Requirements

    Identify Topics from a Timestamped Transcript:
        Extract meaningful topics (themes, concepts) that occur throughout the conversation.
        Topics can be products, features, policies, or recurring issues.

    Determine Topic Sentiment Over Time:
        Assign a polarity score (between -1.0 and 1.0) to each topic mention when it appears or changes in sentiment.
        Use thresholds to categorize sentiment at each mention:
            negative if score < -0.3
            neutral if -0.3 ≤ score ≤ 0.3
            positive if score > 0.3
        Instead of averaging all sentiments over time, record changes in sentiment as they occur:
            If a topic’s sentiment shifts during the conversation, reflect that progression.
            Consider early positive references that later become negative or vice versa—each shift is captured as a separate entry in the topic’s history.

    Timestamp Awareness & Sentiment History:
        For each topic, maintain a history array.
        Each entry in history should reflect:
            The timestamp of when that sentiment was expressed or detected.
            The polarity score and suggested sentiment at that point in time.
        If the topic sentiment does not change, history can have a single entry.
        If it does change, add new entries to history whenever a shift occurs, reflecting the evolving sentiment landscape.

    Output Format & Data Preservation:
        Output only a JSON object with a topics array.
        Each topic object should contain:
            id: A unique identifier (e.g., "topic-1", "topic-2")
            text: The topic’s name or descriptor
            score: A relevance or importance score for the topic (a float you can estimate or keep constant)
            history: An array of objects, each with:
                timestamp: The ISO 8601 timestamp or an approximate time marker from the transcript
                sentiment: An object containing:
                    polarity.score: The float score at that time
                    suggested: "negative", "neutral", or "positive" based on thresholds
        Do not add explanations or reasoning in the output. Just return the JSON.

    Chain-of-Thought (Reasoning) Step:
        Reason silently and do not include reasoning in the final output.
        Internally consider how the topic sentiment changes as the transcript progresses.
        Identify transitions: when a topic’s sentiment goes from positive to neutral, neutral to negative, or any other shift.

    Uncertain Cases:
        If a topic’s sentiment is indeterminable, default to a neutral sentiment (0.0).
        If thresholds seem slightly off, you may lean towards neutral or re-calibrate internally. No commentary.

    No Additional Commentary:
        Only return the final JSON structure.
        Ensure the JSON is well-formed and follows the specified format.

Prompt Reiteration for Clarity

    You are a CX sentiment analysis expert.
    You receive a timestamped transcript.
    You identify topics and track their sentiment changes over time.
    You produce a JSON with topics, each having a history array detailing sentiment shifts.
    No commentary, just the final JSON.

    
Here are some examples:
2024-07-10T11:15:00Z [Customer]: I love the new mobile app interface, it’s fantastic!
2024-07-10T11:20:30Z [Customer]: The pricing options, however, are too steep for my budget.
2024-07-10T11:25:45Z [Customer]: Actually, after using the app more, the interface feels cluttered now.
2024-07-10T11:30:10Z [Customer]: I’m starting to think the pricing might be fair given all the features.

Here is the JSON output:
{
  "topics": [
    {
      "id": "topic-1",
      "text": "mobile app interface",
      "score": 0.8,
      "history": [
        {
          "timestamp": "2024-07-10T11:15:00Z",
          "sentiment": {
            "polarity": {
              "score": 0.7
            },
            "suggested": "positive"
          }
        },
        {
          "timestamp": "2024-07-10T11:25:45Z",
          "sentiment": {
            "polarity": {
              "score": -0.4
            },
            "suggested": "negative"
          }
        }
      ]
    },
    {
      "id": "topic-2",
      "text": "pricing options",
      "score": 0.7,
      "history": [
        {
          "timestamp": "2024-07-10T11:20:30Z",
          "sentiment": {
            "polarity": {
              "score": -0.5
            },
            "suggested": "negative"
          }
        },
        {
          "timestamp": "2024-07-10T11:30:10Z",
          "sentiment": {
            "polarity": {
              "score": 0.2
            },
            "suggested": "neutral"
          }
        }
      ]
    }
  ]
}
"""

USER_PROMPT = "Analyze the following timestamped transcript. Identify all key topics, track their sentiment changes over time (adding a new history entry each time a sentiment shift occurs). Respond only with valid JSON. Do not write an introduction or summary."


def load_csv(num_rows):
    """
    Load the cleaned data from the CSV file
    """
    tqdm.pandas(desc="Progress")
    print(f"Loading {num_rows} rows from: {USER_DATA_CSV}...", end="")

    df = pd.read_csv(USER_DATA_CSV, nrows=num_rows)
    print("Done")

    data = []
    for _, row in tqdm(df.iterrows(), total=len(df)):
        row_str = f"{row['Timestamp']} {row['Speaker Label']} {row['Utterance']}"
        # print("row_str = ", row_str)
        data.append(row_str)
    return data



def run_inference(transcript_list, chunk_size, debug):
    """
    Run batches of inference on the transcript list
    """

    sampling_params = SamplingParams(
        temperature=0.8, 
        top_p=0.95,
        max_tokens=2048,
    )

    # Create an LLM.
    llm = LLM(MODEL_NAME, tensor_parallel_size=2)

    results = ""

    print(f"Processing data...length: {len(transcript_list)}")

    for i in range(0, len(transcript_list), chunk_size):
        
        if i + chunk_size > len(transcript_list):
            chunk_size = len(transcript_list) - i

        print(f"Processing chunk...{i} to {i + chunk_size}")

        transcript = "\n".join(transcript_list[i:i + chunk_size])

        chunk_user_prompt = f"{USER_PROMPT}\n{transcript}"

        if debug:
            print("chunk_user_prompt size:", len(chunk_user_prompt))
            print("SYSTEM_PROMPT size:", len(SYSTEM_PROMPT))

        prompt = (
            "<|begin_of_text|>"
            "<|start_header_id|>system<|end_header_id|>\n"
            f"{SYSTEM_PROMPT}\n"
            "<|eot_id|>"
            "<|start_header_id|>user<|end_header_id|>\n"
            f"{chunk_user_prompt}\n"
            "<|eot_id|>"
            "<|start_header_id|>assistant<|end_header_id|>\n"
        )

        outputs = llm.generate(prompt, sampling_params)
        
        for output in outputs:
            results = results + output.outputs[0].text

    return results

def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description="Runs batch inference on chat conversations.")
    parser.add_argument("--rows", type=int, default=1000, help="Rows to load from .csv.")
    parser.add_argument("--chunk", type=int, default=75, help="Number of rows to pass to inference.")
    parser.add_argument("--debug", action="store_true", help="turn on debugging.")
    args = parser.parse_args()

    # Create a sampling params object.
    
    transcript_list = load_csv(args.rows)
    results_json_string = run_inference(transcript_list, args.chunk, args.debug)

    if args.debug:
        print("Results:", results_json_string)

    # Write results to JSON file
    json_file_path = 'infer_results.json'

    try: 
        with open(json_file_path, "w") as file:
            file.write(results_json_string)
            print(f"Results written to {json_file_path}")
    except Exception as e:
        print(f"Error writing results to {json_file_path}: {e}")

if __name__ == "__main__":
    main()