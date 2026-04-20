PROJECT_SEED_DATA = [
    {
        "title_en": "QR-Based User Authentication System",
        "title_de": "QR-basiertes Nutzerauthentifizierungssystem",
        "summary_en": (
            "Designed and implemented a ROS 2-based user authorization node that supports server login IDs, "
            "QR-code authentication, and manual input using Intel RealSense D455 RGB image streams."
        ),
        "summary_de": (
            "Entwarf und implementierte einen ROS-2-basierten Nutzerautorisierungsknoten, der Server-Login-IDs, "
            "QR-Code-Authentifizierung und manuelle Eingabe mit RGB-Bildstroemen der Intel RealSense D455 unterstuetzt."
        ),
        "impact_en": (
            "Decoded QR codes with OpenCV and pyzbar, filtered invalid scans, tracked authentication state, "
            "and published status to ROS topics to control robot actions such as door unlocking."
        ),
        "impact_de": (
            "Dekodierte QR-Codes mit OpenCV und pyzbar, filterte ungueltige Scans, verfolgte den Authentifizierungsstatus "
            "und publizierte den Zustand auf ROS-Topics zur Steuerung von Roboteraktionen wie dem Oeffnen der Tuer."
        ),
        "tech_stack": ["ROS 2", "OpenCV", "pyzbar", "Intel RealSense D455", "Python", "User Authorization"],
        "timeframe": "Dec 2025 - Jan 2026",
        "category": "Robot Authorization",
        "featured": True,
        "live_url": "",
        "repo_url": "",
    },
    {
        "title_en": "ElDrive - Autonomous Shuttle for Elderly Users in Bavarian Region",
        "title_de": "ElDrive - Autonomer Shuttle fuer aeltere Nutzer in Bayern",
        "summary_en": (
            "Identified user needs through Human-Centered Design, created story maps and system architecture, "
            "and implemented ROS 2 interfaces and core functionality with a six-member agile team."
        ),
        "summary_de": (
            "Identifizierte Nutzerbeduerfnisse mit einem Human-Centered-Design-Ansatz, entwickelte Story Maps "
            "und Systemarchitektur und implementierte ROS-2-Schnittstellen sowie Kernfunktionen in einem sechskopfigen agilen Team."
        ),
        "impact_en": (
            "Contributed to ROS 2 interfaces across localization, path planning, trajectory control, "
            "human-machine interfaces, user authorization, and decision-making modules, served as Scrum Master, "
            "and helped prepare the stack for testing and deployment in Model City."
        ),
        "impact_de": (
            "Unterstuetzte ROS-2-Schnittstellen fuer Lokalisierung, Pfadplanung, Trajektorienregelung, "
            "Mensch-Maschine-Schnittstellen, Nutzerautorisierung und Entscheidungslogik, uebernahm die Rolle "
            "des Scrum Masters und bereitete den Stack auf Tests und Deployment in Model City vor."
        ),
        "tech_stack": ["ROS 2", "Human-Centered Design", "Agile", "System Architecture", "UML", "Gitea"],
        "timeframe": "Mar 2025 - Feb 2026",
        "category": "Autonomous Shuttle Systems",
        "featured": True,
        "live_url": "",
        "repo_url": "",
    },
    {
        "title_en": "Heavy-Transport Route Planning Platform",
        "title_de": "Plattform fuer Schwertransport-Routenplanung",
        "summary_en": (
            "Built a FastAPI-driven planning workflow that combines permit extraction, bridge "
            "matching, geospatial transforms, and an interactive Leaflet map for restricted-route analysis."
        ),
        "summary_de": (
            "Entwickelte einen FastAPI-gestuetzten Planungsablauf, der Genehmigungsextraktion, "
            "Brueckenabgleich, Geotransformationen und eine interaktive Leaflet-Karte fuer die Analyse "
            "eingeschraenkter Routen verbindet."
        ),
        "impact_en": (
            "Turned official transport permits into structured SQLite constraints and generated safer alternative truck routes."
        ),
        "impact_de": (
            "Wandelte offizielle Transportgenehmigungen in strukturierte SQLite-Einschraenkungen um und erzeugte sicherere alternative Lkw-Routen."
        ),
        "tech_stack": ["FastAPI", "SQLite", "Leaflet.js", "OpenRouteService", "OpenStreetMap", "pdfplumber"],
        "timeframe": "Aug 2025 - Present",
        "category": "Mobility Systems",
        "featured": True,
        "live_url": "",
        "repo_url": "",
    },
    {
        "title_en": "Autonomous Shuttle HMI Suite",
        "title_de": "HMI-Suite fuer autonomen Shuttle",
        "summary_en": (
            "Designed external and in-shuttle interfaces connected to ROS 2 through rosbridge WebSockets "
            "for booking, journey updates, help flows, and ride cancellation."
        ),
        "summary_de": (
            "Konzipierte externe und fahrzeuginterne Oberflaechen, die ueber rosbridge WebSockets mit ROS 2 "
            "verbunden sind, fuer Buchung, Fahrstatus, Hilfefunktionen und Stornierung."
        ),
        "impact_en": (
            "Created elderly-friendly human-machine interfaces that translated live ROS topics into clear passenger interactions."
        ),
        "impact_de": (
            "Entwickelte seniorenfreundliche Mensch-Maschine-Schnittstellen, die Live-ROS-Themen in klare Fahrgastinteraktionen uebersetzen."
        ),
        "tech_stack": ["ROS 2", "JavaScript", "WebSockets", "Figma", "Jest", "Human-Centered Design"],
        "timeframe": "Mar 2025 - Feb 2026",
        "category": "Human-Machine Interfaces",
        "featured": True,
        "live_url": "",
        "repo_url": "",
    },
    {
        "title_en": "Landmark-Based Autonomous Navigation",
        "title_de": "Merkmalsbasierte autonome Navigation",
        "summary_en": (
            "Implemented a full perception-to-control pipeline using YOLOv8, RGB-D sensing, pylon pairing, "
            "pure pursuit control, and OptiTrack feedback for a model vehicle."
        ),
        "summary_de": (
            "Implementierte eine vollstaendige Wahrnehmungs-bis-Regelungs-Pipeline mit YOLOv8, RGB-D-Sensorik, "
            "Pylonen-Paarung, Pure-Pursuit-Regelung und OptiTrack-Feedback fuer ein Modellfahrzeug."
        ),
        "impact_en": (
            "Delivered stable autonomous driving up to 1.5 m/s and quantified how curvature and landmark spacing affect performance."
        ),
        "impact_de": (
            "Ermoeglichte stabiles autonomes Fahren bis 1,5 m/s und quantifizierte den Einfluss von Kruemmung und Landmarkenabstand auf die Leistung."
        ),
        "tech_stack": ["Python", "ROS 2", "YOLOv8", "Intel RealSense", "OptiTrack", "Pure Pursuit"],
        "timeframe": "Jan 2026 - Feb 2026",
        "category": "Autonomous Driving",
        "featured": True,
        "live_url": "",
        "repo_url": "",
    },
    {
        "title_en": "Glass Manufacturing Analytics and AI Chatbot",
        "title_de": "Glasfertigungs-Analytics und KI-Chatbot",
        "summary_en": (
            "Built a Streamlit analytics system backed by SQLite, Random Forest defect prediction, and "
            "a chatbot that translates natural language questions into production insights."
        ),
        "summary_de": (
            "Entwickelte ein Streamlit-Analysesystem mit SQLite, Random-Forest-Fehlervorhersage und "
            "einem Chatbot, der natuerliche Fragen in Produktions-Insights uebersetzt."
        ),
        "impact_en": (
            "Combined SQL analysis, machine learning, and dashboard UX into one end-to-end industrial decision-support prototype."
        ),
        "impact_de": (
            "Kombinierte SQL-Analyse, maschinelles Lernen und Dashboard-UX zu einem durchgaengigen industriellen Entscheidungsunterstuetzungs-Prototyp."
        ),
        "tech_stack": ["Streamlit", "SQLite", "Random Forest", "Pandas", "scikit-learn", "SQL"],
        "timeframe": "2024",
        "category": "Data and AI",
        "featured": True,
        "live_url": "",
        "repo_url": "",
    },
    {
        "title_en": "Real-Time Object Detection on Model Car",
        "title_de": "Echtzeit-Objekterkennung auf Modellfahrzeug",
        "summary_en": (
            "Captured and annotated a 1,294-image dataset, fine-tuned MobileNet SSD v1, and deployed the "
            "optimized ONNX model on an Nvidia Jetson-powered model car."
        ),
        "summary_de": (
            "Erfasste und annotierte einen Datensatz mit 1.294 Bildern, optimierte MobileNet SSD v1 "
            "und deployte das verbesserte ONNX-Modell auf einem Nvidia-Jetson-basierten Modellfahrzeug."
        ),
        "impact_en": (
            "Raised mean average precision from 0.51 to 0.84 for more robust detection under model-city conditions."
        ),
        "impact_de": (
            "Steigerte die mittlere durchschnittliche Praezision von 0,51 auf 0,84 fuer robustere Erkennung unter Model-City-Bedingungen."
        ),
        "tech_stack": ["Computer Vision", "MobileNet SSD", "Roboflow", "ONNX", "Nvidia Jetson"],
        "timeframe": "Jun 2025 - Jul 2025",
        "category": "Perception AI",
        "featured": True,
        "live_url": "",
        "repo_url": "",
    },
]
