# Robotic Data Preprocessing
## Installation
```bash
cd ~/dev_ws/
git clone <repo_url>
```

Make sure to download this folder in the same root directory of the MRS simulation.

**Python dependencies**:
```bash
pip install pipreqs
pipreqs .
pip install -r requirements.txt
```

## Run
- Option 1:
    ```bash
    python converter.py
    python preprocess.py
    ```

- Option 2:

    Automatically executed at the end of a MRS simulation. See [simulation launch file](https://bitbucket.org/proslabteam/smart_agriculture_sim/src/master/single_launch.sh).