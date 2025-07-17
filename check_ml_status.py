from src.ml_predictive_engine import get_ml_engine

def check_ml_status():
    ml = get_ml_engine()
    print("Current ML Engine Status:")
    print(f"Metrics collected: {len(ml['data_collector'].metrics)}")
    print(f"Actions collected: {len(ml['data_collector'].actions)}")
    print(f"System optimizer trained: {ml['system_optimizer'].is_trained}")
    
    # Show a sample of recent metrics if available
    if ml['data_collector'].metrics:
        print("\nSample of recent metrics:")
        for i, metric in enumerate(ml['data_collector'].metrics[-5:]):  # Last 5 metrics
            print(f"  {i+1}. {metric}")
    
    # Show a sample of recent actions if available
    if ml['data_collector'].actions:
        print("\nSample of recent actions:")
        for i, action in enumerate(ml['data_collector'].actions[-5:]):  # Last 5 actions
            print(f"  {i+1}. {action}")

if __name__ == "__main__":
    check_ml_status()
