from src.utils.singleton import Falcon

class ModelManager:
    """Manages model instances using singleton pattern"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
            cls._instance._model_type = None
        return cls._instance
    
    def initialize(self, model_type: str = "falcon"):
        """Initialize model if not already initialized"""
        if self._model is None:
            self._model_type = model_type.lower()
            print(f"\nInitializing {model_type} model...")
            try:
                self._model = Falcon(model_type)
                print(f"✓ {model_type} model loaded successfully")
            except Exception as e:
                print(f"✗ Error loading {model_type} model: {e}")
                raise
            print("Model initialization complete!")
    
    def get_model(self):
        """Get the model instance, initializing if needed"""
        if self._model is None:
            self.initialize()
        return self._model

