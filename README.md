## How to use

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
2. Run the benchmarks you want. For example, to run the Typesense Vamana benchmark:

    ```bash
    python run.py  --algorithm=typesenseVamana --local  --runs 1
    ```
4. Plot the results:

    ```bash
    python plot.py
    ```