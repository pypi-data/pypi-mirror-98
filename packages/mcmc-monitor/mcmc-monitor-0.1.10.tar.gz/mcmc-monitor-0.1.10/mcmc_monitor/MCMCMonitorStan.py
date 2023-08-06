import os
import time
import tempfile
import shutil
from typing import List
from .workspace import load_workspace
from .monitor_stan_run import monitor_stan_run, finalize_monitor_stan_run

class MCMCMonitorStan():
    def __init__(self, *, run_label: str, parameter_keys: List[str], run_metadata: dict={}, workspace_uri: str='default', output_dir=None):
        self._workspace_uri = workspace_uri
        self._run_label = run_label
        self._parameter_keys = parameter_keys
        self._run_metadata = run_metadata
        self.output_dir = output_dir
        self._prefix = 'mcmc-monitor-'

    def __enter__(self):
        if self.output_dir is None:
            dirpath = None
            self.output_dir = str(tempfile.mkdtemp(
                prefix=self._prefix, dir=dirpath))
            self._remove = True
        else:
            self._remove = False
        
        # Load the default mcmc-monitor workspace and create a new run
        monitor_workspace = load_workspace(self._workspace_uri)
        run_id = monitor_workspace.add_run(label=self._run_label, metadata=self._run_metadata)
        # begin monitoring the output directory for this run
        monitor_stan_run(
            monitor_workspace.get_run(run_id),
            self.output_dir,
            self._parameter_keys
        )
        print('========================================================')
        print(f'Monitoring stan run in directory: {self.output_dir}')
        print(f'Workspace URI: {monitor_workspace.get_workspace_uri()}')
        print(f'Run ID: {run_id}')
        url = os.getenv('MCMC_MONITOR_URL', None)
        if not url:
            print('Environment variable not set: MCMC_MONITOR_URL')
            url = '<MCMC_MONITOR_URL>'
        print(f'{url}/run/{run_id}?workspace={monitor_workspace.get_workspace_uri()}')
        print('========================================================')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # allow monitoring to finish before removing directory
        print(f'Finalizing monitoring of stan run in directory: {self.output_dir}')
        finalize_monitor_stan_run(self.output_dir)
        if self._remove:
            _rmdir_with_retries(self.output_dir, num_retries=5)

    def workspace_uri(self):
        return self._workspace_uri

    def path(self):
        return self._path

def _rmdir_with_retries(dirname: str, num_retries: int, delay_between_tries: float=1):
    for retry_num in range(1, num_retries + 1):
        if not os.path.exists(dirname):
            return
        try:
            shutil.rmtree(dirname)
            break
        except: # pragma: no cover
            if retry_num < num_retries:
                print('Retrying to remove directory: {}'.format(dirname))
                time.sleep(delay_between_tries)
            else:
                raise Exception('Unable to remove directory after {} tries: {}'.format(num_retries, dirname))
