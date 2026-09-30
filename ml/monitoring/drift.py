import pandas as pd
import numpy as np
from scipy.spatial.distance import jensenshannon
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_drift(reference_data_path, current_data_path, threshold=0.1):
    """
    Detect job-market drift by comparing old JDs (reference) vs new JDs (current).
    Uses a simple length distribution comparison as a proxy, or placeholder for TF-IDF/Embeddings drift.
    """
    logger.info("Loading reference and current job description data...")
    try:
        ref_df = pd.read_csv(reference_data_path)
        cur_df = pd.read_csv(current_data_path)
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return
        
    # Placeholder: Assuming a feature 'jd_length' exists or we compute it
    if 'job_description' in ref_df.columns:
        ref_df['jd_length'] = ref_df['job_description'].apply(len)
        cur_df['jd_length'] = cur_df['job_description'].apply(len)
        
        # Calculate histograms for JS divergence
        ref_hist, bins = np.histogram(ref_df['jd_length'], bins=50, density=True)
        cur_hist, _ = np.histogram(cur_df['jd_length'], bins=bins, density=True)
        
        # Add small epsilon to avoid zero probabilities
        eps = 1e-10
        ref_hist = ref_hist + eps
        cur_hist = cur_hist + eps
        
        # Normalize
        ref_hist /= ref_hist.sum()
        cur_hist /= cur_hist.sum()
        
        js_div = jensenshannon(ref_hist, cur_hist)
        
        logger.info(f"Jensen-Shannon Divergence: {js_div:.4f}")
        
        if js_div > threshold:
            logger.warning(f"Drift detected! JS Divergence ({js_div:.4f}) exceeds threshold ({threshold}).")
        else:
            logger.info("No significant drift detected.")
            
        return js_div
    else:
        logger.error("Column 'job_description' not found in data.")
        return None

if __name__ == "__main__":
    # Mock data paths for demonstration
    # detect_drift('data/reference_jds.csv', 'data/current_jds.csv')
    pass
