from src.utils.singleton import Falcon

class ModelManager:
    """Manages model instances using singleton pattern"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
        return cls._instance
    
    def initialize(self):
        """Initialize model if not already initialized"""
        if self._model is None:
            print("\nInitializing Falcon model...")
            try:
                self._model = Falcon()
                print("✓ Falcon model loaded successfully")
            except Exception as e:
                print(f"✗ Error loading Falcon model: {e}")
                raise
            print("Model initialization complete!")
    
    def get_model(self):
        """Get the model instance, initializing if needed"""
        if self._model is None:
            self.initialize()
        return self._model

