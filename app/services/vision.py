from ultralytics import YOLOWorld
from app.services.rag import rag_engine


# ============================================================
# YOLO-WORLD MODEL
# ============================================================

model = YOLOWorld("yolov8s-worldv2.pt")


# ============================================================
# ENGINEERING COMPONENT VOCABULARY
# ============================================================

COMPONENTS = [
    "miniature circuit breaker",
    "electrical circuit breaker",
    "breaker switch",
    "electrical switch",
    "contactor",
    "electrical relay",
    "relay",
    "fuse",
    "fuse holder",
    "terminal block",
    "electrical control panel",
    "electrical panel",
    "transformer",
    "electric motor",
]


# Tell YOLO-World what objects we are interested in
model.set_classes(COMPONENTS)


# ============================================================
# MAP DETECTION NAMES TO OUR KNOWLEDGE BASE
# ============================================================

RAG_MAPPING = {
    "miniature circuit breaker": "MCB",
    "electrical circuit breaker": "Circuit Breaker",
    "breaker switch": "Circuit Breaker",
    "electrical switch": "Circuit Breaker",
    "contactor": "Contactor",
    "electrical relay": "Relay",
    "relay": "Relay",
}


# ============================================================
# IMAGE ANALYSIS
# ============================================================

def analyze_image(image_path: str):

    results = model.predict(
        image_path,
        conf=0.05,
        verbose=True
    )

    detections = []
    knowledge = []

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])

            confidence = float(box.conf[0])

            object_name = result.names[class_id]

            # -----------------------------------------
            # Detection result
            # -----------------------------------------

            detections.append({
                "object": object_name,
                "confidence": round(confidence, 3)
            })

            # -----------------------------------------
            # RAG lookup
            # -----------------------------------------

            rag_name = RAG_MAPPING.get(object_name)

            if rag_name:

                retrieved = rag_engine.search(
                    rag_name,
                    top_k=1
                )

                if retrieved:

                    knowledge.append({
                        "detected_object": object_name,
                        "confidence": round(confidence, 3),
                        "knowledge": retrieved[0]
                    })

    return {
        "success": True,
        "detections": detections,
        "knowledge": knowledge
    }