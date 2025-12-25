## How to use

1. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Install benchmark_algorithms as a package:

   ```bash
   pip install -e ../benchmark_algorithms/
   ```
4. Install typesense package:

   ```bash
   pip install typesense
   ```
5. Run the benchmarks you want. For example, to run the Typesense Vamana benchmark:

    ```bash
    python run.py  --algorithm=typesenseVamana --local  --runs 1
    ```
6. Plot the results:

    ```bash
    python plot.py
    ```