"""
EVE Language Module
Multi-language support for EVE AI Assistant
"""

from typing import Dict, Any, Optional
import json
import os

LANG_DIR = os.path.join(os.path.dirname(__file__), 'languages')

# Language codes and names
LANGUAGES = {
    'en': {'name': 'English', 'native': 'English'},
    'sn': {'name': 'Shona', 'native': 'Shona'},
    'ja': {'name': 'Japanese', 'native': '日本語'},
    'ko': {'name': 'Korean', 'native': '한국어'},
    'ru': {'name': 'Russian', 'native': 'Русский'},
    'zh': {'name': 'Chinese', 'native': '中文'},
    'es': {'name': 'Spanish', 'native': 'Español'},
    'fr': {'name': 'French', 'native': 'Français'},
    'de': {'name': 'German', 'native': 'Deutsch'},
    'pt': {'name': 'Portuguese', 'native': 'Português'},
    'ar': {'name': 'Arabic', 'native': 'العربية'},
    'hi': {'name': 'Hindi', 'native': 'हिन्दी'},
    'sw': {'name': 'Swahili', 'native': 'Kiswahili'},
    'zu': {'name': 'Zulu', 'native': 'Zulu'},
}

# Translation dictionaries
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'en': {
        # Core UI
        'app_name': 'EVE AI',
        'tagline': 'Your Universal AI Assistant',
        
        # Navigation
        'nav_chat': 'Chat',
        'nav_tools': 'Tools',
        'nav_memory': 'Memory',
        'nav_settings': 'Settings',
        
        # Chat
        'input_placeholder': 'Message EVE...',
        'send': 'Send',
        'thinking': 'Thinking...',
        
        # Greetings
        'greeting': 'Hello! I am EVE, your universal AI assistant.',
        'capabilities': 'I can help you with:',
        'what_can_i_do': 'What would you like me to help you with today?',
        
        # Tools
        'tools_title': 'Tools & Capabilities',
        'web_search': 'Web Search',
        'web_browse': 'Web Browser',
        'file_read': 'Read Files',
        'file_write': 'Write Files',
        'code_execute': 'Execute Code',
        'command_run': 'Run Commands',
        
        # Security
        'security_title': 'Security Tools',
        'port_scan': 'Port Scanner',
        'dns_lookup': 'DNS Lookup',
        'whois': 'WHOIS Lookup',
        'ssl_analysis': 'SSL Analysis',
        'headers_check': 'Security Headers',
        'password_check': 'Password Strength',
        'hash_identify': 'Hash Identifier',
        
        # Settings
        'settings_title': 'Settings',
        'language': 'Language',
        'voice': 'Voice',
        'api_key': 'API Key',
        'theme': 'Theme',
        
        # Status
        'online': 'Online',
        'offline': 'Offline',
        'processing': 'Processing',
        
        # Errors
        'error': 'Error',
        'success': 'Success',
        
        # Actions
        'save': 'Save',
        'cancel': 'Cancel',
        'delete': 'Delete',
        'clear': 'Clear',
        'create': 'Create',
        'rename': 'Rename',
    },
    
    'sn': {  # Shona
        'app_name': 'EVE AI',
        'tagline': 'Mushandisi wako weAI wehurunza',
        
        'nav_chat': 'Mhosho',
        'nav_tools': 'Mitauro',
        'nav_memory': 'M记忆',
        'nav_settings': 'Mabhesedhi',
        
        'input_placeholder': 'MESSAGE EVE...',
        'send': 'Tumira',
        'thinking': 'Kufunga...',
        
        'greeting': 'Mhoro! ini ndiri EVE, mushandisi weAI wehurunza.',
        'capabilities': 'Ndiko kugona kukubatsira:',
        'what_can_i_do': 'Unoda ndikubatsirei nhasi?',
        
        'tools_title': 'Mitauro & Zvigamuchidzo',
        'web_search': 'Rima',
        'web_browse': 'Web Browser',
        'file_read': 'Verenga Mafaira',
        'file_write': 'Nyora Mafaira',
        'code_execute': 'Tenda Kodhi',
        'command_run': 'Tenda Commands',
        
        'security_title': 'Maitiro EkuSecurity',
        'port_scan': 'Port Scanner',
        'dns_lookup': 'DNS Lookup',
        'whois': 'WHOIS Lookup',
        'ssl_analysis': 'SSL Analysis',
        'headers_check': 'Security Headers',
        'password_check': 'Password Strength',
        'hash_identify': 'Hash Identifier',
        
        'settings_title': 'Mabhesedhi',
        'language': 'Chirungu',
        'voice': 'Voice',
        'api_key': 'API Key',
        'theme': 'Theme',
        
        'online': 'Online',
        'offline': 'Offline',
        'processing': 'Processing',
        
        'error': 'Kukanganisa',
        'success': 'Mabasa',
        
        'save': 'Chengeta',
        'cancel': 'Kanzura',
        'delete': 'Delete',
        'clear': 'Clear',
        'create': 'Create',
        'rename': 'Rename',
    },
    
    'ja': {  # Japanese
        'app_name': 'EVE AI',
        'tagline': 'あなたのユニバーサルAIアシスタント',
        
        'nav_chat': 'チャット',
        'nav_tools': 'ツール',
        'nav_memory': 'メモリ',
        'nav_settings': '設定',
        
        'input_placeholder': 'EVEにメッセージ...',
        'send': '送信',
        'thinking': '考え中...',
        
        'greeting': 'こんにちは！私はEVEです、あなたのユニバーサルAIアシスタント。',
        'capabilities': '私はこれら帮助你できます：',
        'what_can_i_do': '今日は何をお手伝いしましょうか？',
        
        'tools_title': 'ツール＆機能',
        'web_search': 'ウェブ検索',
        'web_browse': 'ウェブブラウザー',
        'file_read': 'ファイルを読む',
        'file_write': 'ファイルを書き込む',
        'code_execute': 'コード実行',
        'command_run': 'コマンド実行',
        
        'security_title': 'セキュリティツール',
        'port_scan': 'ポートスキャナー',
        'dns_lookup': 'DNSルックアップ',
        'whois': 'WHOISルックアップ',
        'ssl_analysis': 'SSL分析',
        'headers_check': 'セキュリティヘッダー',
        'password_check': 'パスワード強度',
        'hash_identify': 'ハッシュ識別',
        
        'settings_title': '設定',
        'language': '言語',
        'voice': '音声',
        'api_key': 'APIキー',
        'theme': 'テーマ',
        
        'online': 'オンライン',
        'offline': 'オフライン',
        'processing': '処理中',
        
        'error': 'エラー',
        'success': '成功',
        
        'save': '保存',
        'cancel': 'キャンセル',
        'delete': '削除',
        'clear': 'クリア',
        'create': '作成',
        'rename': '名前変更',
    },
    
    'ko': {  # Korean
        'app_name': 'EVE AI',
        'tagline': '당신의 범용 AI 어시스턴트',
        
        'nav_chat': '채팅',
        'nav_tools': '도구',
        'nav_memory': '메모리',
        'nav_settings': '설정',
        
        'input_placeholder': 'EVE에게 메시지...',
        'send': '전송',
        'thinking': '생각 중...',
        
        'greeting': '안녕하세요! 저는 EVE입니다, 당신의 범용 AI 어시스턴트.',
        'capabilities': '저는 이것들을 도와드릴 수 있습니다:',
        'what_can_i_do': '오늘 무엇을 도와드릴까요?',
        
        'tools_title': '도구 및 기능',
        'web_search': '웹 검색',
        'web_browse': '웹 브라우저',
        'file_read': '파일 읽기',
        'file_write': '파일 쓰기',
        'code_execute': '코드 실행',
        'command_run': '명령어 실행',
        
        'security_title': '보안 도구',
        'port_scan': '포트 스캐너',
        'dns_lookup': 'DNS 조회',
        'whois': 'WHOIS 조회',
        'ssl_analysis': 'SSL 분석',
        'headers_check': '보안 헤더',
        'password_check': '비밀번호 강도',
        'hash_identify': '해시 식별',
        
        'settings_title': '설정',
        'language': '언어',
        'voice': '음성',
        'api_key': 'API 키',
        'theme': '테마',
        
        'online': '온라인',
        'offline': '오프라인',
        'processing': '처리 중',
        
        'error': '오류',
        'success': '성공',
        
        'save': '저장',
        'cancel': '취소',
        'delete': '삭제',
        'clear': '지우기',
        'create': '생성',
        'rename': '이름 변경',
    },
    
    'ru': {  # Russian
        'app_name': 'EVE AI',
        'tagline': 'Ваш универсальный ИИ-ассистент',
        
        'nav_chat': 'Чат',
        'nav_tools': 'Инструменты',
        'nav_memory': 'Память',
        'nav_settings': 'Настройки',
        
        'input_placeholder': 'Сообщение EVE...',
        'send': 'Отправить',
        'thinking': 'Думаю...',
        
        'greeting': 'Привет! Я EVE, ваш универсальный ИИ-ассистент.',
        'capabilities': 'Я могу помочь вам с:',
        'what_can_i_do': 'Чем бы вы хотели, чтобы я помогла сегодня?',
        
        'tools_title': 'Инструменты и возможности',
        'web_search': 'Веб-поиск',
        'web_browse': 'Веб-браузер',
        'file_read': 'Чтение файлов',
        'file_write': 'Запись файлов',
        'code_execute': 'Выполнение кода',
        'command_run': 'Выполнение команд',
        
        'security_title': 'Инструменты безопасности',
        'port_scan': 'Сканер портов',
        'dns_lookup': 'DNS-запрос',
        'whois': 'WHOIS-запрос',
        'ssl_analysis': 'SSL анализ',
        'headers_check': 'Заголовки безопасности',
        'password_check': 'Проверка пароля',
        'hash_identify': 'Идентификация хеша',
        
        'settings_title': 'Настройки',
        'language': 'Язык',
        'voice': 'Голос',
        'api_key': 'API ключ',
        'theme': 'Тема',
        
        'online': 'Онлайн',
        'offline': 'Офлайн',
        'processing': 'Обработка',
        
        'error': 'Ошибка',
        'success': 'Успех',
        
        'save': 'Сохранить',
        'cancel': 'Отмена',
        'delete': 'Удалить',
        'clear': 'Очистить',
        'create': 'Создать',
        'rename': 'Переименовать',
    },
    
    'zh': {  # Chinese
        'app_name': 'EVE AI',
        'tagline': '您的通用AI助手',
        
        'nav_chat': '聊天',
        'nav_tools': '工具',
        'nav_memory': '记忆',
        'nav_settings': '设置',
        
        'input_placeholder': '发消息给EVE...',
        'send': '发送',
        'thinking': '思考中...',
        
        'greeting': '你好！我是EVE，您的通用AI助手。',
        'capabilities': '我可以帮助您：',
        'what_can_i_do': '今天有什么可以帮您的？',
        
        'tools_title': '工具和功能',
        'web_search': '网页搜索',
        'web_browse': '网页浏览',
        'file_read': '读取文件',
        'file_write': '写入文件',
        'code_execute': '执行代码',
        'command_run': '运行命令',
        
        'security_title': '安全工具',
        'port_scan': '端口扫描',
        'dns_lookup': 'DNS查询',
        'whois': 'WHOIS查询',
        'ssl_analysis': 'SSL分析',
        'headers_check': '安全头检查',
        'password_check': '密码强度',
        'hash_identify': '哈希识别',
        
        'settings_title': '设置',
        'language': '语言',
        'voice': '语音',
        'api_key': 'API密钥',
        'theme': '主题',
        
        'online': '在线',
        'offline': '离线',
        'processing': '处理中',
        
        'error': '错误',
        'success': '成功',
        
        'save': '保存',
        'cancel': '取消',
        'delete': '删除',
        'clear': '清除',
        'create': '创建',
        'rename': '重命名',
    },
    
    'es': {  # Spanish
        'app_name': 'EVE AI',
        'tagline': 'Tu Asistente IA Universal',
        
        'nav_chat': 'Chat',
        'nav_tools': 'Herramientas',
        'nav_memory': 'Memoria',
        'nav_settings': 'Ajustes',
        
        'input_placeholder': 'Mensaje a EVE...',
        'send': 'Enviar',
        'thinking': 'Pensando...',
        
        'greeting': '¡Hola! Soy EVE, tu asistente IA universal.',
        'capabilities': 'Puedo ayudarte con:',
        'what_can_i_do': '¿Con qué te gustaría que te ayude hoy?',
        
        'tools_title': 'Herramientas y Capacidades',
        'web_search': 'Búsqueda Web',
        'web_browse': 'Navegador Web',
        'file_read': 'Leer Archivos',
        'file_write': 'Escribir Archivos',
        'code_execute': 'Ejecutar Código',
        'command_run': 'Ejecutar Comandos',
        
        'security_title': 'Herramientas de Seguridad',
        'port_scan': 'Escáner de Puertos',
        'dns_lookup': 'Búsqueda DNS',
        'whois': 'Búsqueda WHOIS',
        'ssl_analysis': 'Análisis SSL',
        'headers_check': 'Cabeceras de Seguridad',
        'password_check': 'Contraseña',
        'hash_identify': 'Identificador de Hash',
        
        'settings_title': 'Ajustes',
        'language': 'Idioma',
        'voice': 'Voz',
        'api_key': 'Clave API',
        'theme': 'Tema',
        
        'online': 'En línea',
        'offline': 'Desconectado',
        'processing': 'Procesando',
        
        'error': 'Error',
        'success': 'Éxito',
        
        'save': 'Guardar',
        'cancel': 'Cancelar',
        'delete': 'Eliminar',
        'clear': 'Limpiar',
        'create': 'Crear',
        'rename': 'Renombrar',
    },
    
    'fr': {  # French
        'app_name': 'EVE AI',
        'tagline': 'Votre Assistant IA Universel',
        
        'nav_chat': 'Chat',
        'nav_tools': 'Outils',
        'nav_memory': 'Mémoire',
        'nav_settings': 'Paramètres',
        
        'input_placeholder': 'Message à EVE...',
        'send': 'Envoyer',
        'thinking': 'Réflexion...',
        
        'greeting': 'Bonjour! Je suis EVE, votre assistant IA universel.',
        'capabilities': 'Je peux vous aider avec:',
        'what_can_i_do': 'Avec quoi aimeriez-vous que je vous aide aujourd\'hui?',
        
        'tools_title': 'Outils et Capacités',
        'web_search': 'Recherche Web',
        'web_browse': 'Navigateur Web',
        'file_read': 'Lire Fichiers',
        'file_write': 'Écrire Fichiers',
        'code_execute': 'Exécuter Code',
        'command_run': 'Exécuter Commandes',
        
        'security_title': 'Outils de Sécurité',
        'port_scan': 'Scanner de Ports',
        'dns_lookup': 'Recherche DNS',
        'whois': 'Recherche WHOIS',
        'ssl_analysis': 'Analyse SSL',
        'headers_check': 'En-têtes Sécurité',
        'password_check': 'Mot de Passe',
        'hash_identify': 'Identifiant Hash',
        
        'settings_title': 'Paramètres',
        'language': 'Langue',
        'voice': 'Voix',
        'api_key': 'Clé API',
        'theme': 'Thème',
        
        'online': 'En ligne',
        'offline': 'Hors ligne',
        'processing': 'Traitement',
        
        'error': 'Erreur',
        'success': 'Succès',
        
        'save': 'Sauvegarder',
        'cancel': 'Annuler',
        'delete': 'Supprimer',
        'clear': 'Effacer',
        'create': 'Créer',
        'rename': 'Renommer',
    },
    
    'de': {  # German
        'app_name': 'EVE AI',
        'tagline': 'Dein Universeller KI-Assistent',
        
        'nav_chat': 'Chat',
        'nav_tools': 'Werkzeuge',
        'nav_memory': 'Speicher',
        'nav_settings': 'Einstellungen',
        
        'input_placeholder': 'Nachricht an EVE...',
        'send': 'Senden',
        'thinking': 'Denke...',
        
        'greeting': 'Hallo! Ich bin EVE, dein universeller KI-Assistent.',
        'capabilities': 'Ich kann dir helfen bei:',
        'what_can_i_do': 'Wobei soll ich dir heute helfen?',
        
        'tools_title': 'Werkzeuge & Fähigkeiten',
        'web_search': 'Websuche',
        'web_browse': 'Webbrowser',
        'file_read': 'Dateien Lesen',
        'file_write': 'Dateien Schreiben',
        'code_execute': 'Code Ausführen',
        'command_run': 'Befehle Ausführen',
        
        'security_title': 'Sicherheitswerkzeuge',
        'port_scan': 'Port-Scanner',
        'dns_lookup': 'DNS-Abfrage',
        'whois': 'WHOIS-Abfrage',
        'ssl_analysis': 'SSL-Analyse',
        'headers_check': 'Sicherheitsheader',
        'password_check': 'Passwortstärke',
        'hash_identify': 'Hash-Identifikation',
        
        'settings_title': 'Einstellungen',
        'language': 'Sprache',
        'voice': 'Stimme',
        'api_key': 'API-Schlüssel',
        'theme': 'Thema',
        
        'online': 'Online',
        'offline': 'Offline',
        'processing': 'Verarbeitung',
        
        'error': 'Fehler',
        'success': 'Erfolg',
        
        'save': 'Speichern',
        'cancel': 'Abbrechen',
        'delete': 'Löschen',
        'clear': 'Leeren',
        'create': 'Erstellen',
        'rename': 'Umbenennen',
    },
    
    'pt': {  # Portuguese
        'app_name': 'EVE AI',
        'tagline': 'Seu Assistente IA Universal',
        
        'nav_chat': 'Chat',
        'nav_tools': 'Ferramentas',
        'nav_memory': 'Memória',
        'nav_settings': 'Configurações',
        
        'input_placeholder': 'Mensagem para EVE...',
        'send': 'Enviar',
        'thinking': 'Pensando...',
        
        'greeting': 'Olá! Eu sou EVE, seu assistente IA universal.',
        'capabilities': 'Posso ajudá-lo com:',
        'what_can_i_do': 'Com o que você gostaria que eu ajudasse hoje?',
        
        'tools_title': 'Ferramentas e Capacidades',
        'web_search': 'Busca Web',
        'web_browse': 'Navegador Web',
        'file_read': 'Ler Arquivos',
        'file_write': 'Escrever Arquivos',
        'code_execute': 'Executar Código',
        'command_run': 'Executar Comandos',
        
        'security_title': 'Ferramentas de Segurança',
        'port_scan': 'Scanner de Portas',
        'dns_lookup': 'Pesquisa DNS',
        'whois': 'Pesquisa WHOIS',
        'ssl_analysis': 'Análise SSL',
        'headers_check': 'Cabeçalhos de Segurança',
        'password_check': 'Senha',
        'hash_identify': 'Identificador de Hash',
        
        'settings_title': 'Configurações',
        'language': 'Idioma',
        'voice': 'Voz',
        'api_key': 'Chave API',
        'theme': 'Tema',
        
        'online': 'Online',
        'offline': 'Offline',
        'processing': 'Processando',
        
        'error': 'Erro',
        'success': 'Sucesso',
        
        'save': 'Salvar',
        'cancel': 'Cancelar',
        'delete': 'Excluir',
        'clear': 'Limpar',
        'create': 'Criar',
        'rename': 'Renomear',
    },
    
    'ar': {  # Arabic
        'app_name': 'EVE AI',
        'tagline': 'مساعد الذكاء الاصطناعي الخاص بك',
        
        'nav_chat': 'محادثة',
        'nav_tools': 'الأدوات',
        'nav_memory': 'الذاكرة',
        'nav_settings': 'الإعدادات',
        
        'input_placeholder': 'رسالة إلى EVE...',
        'send': 'إرسال',
        'thinking': 'جارٍ التفكير...',
        
        'greeting': 'مرحباً! أنا EVE، مساعد الذكاء الاصطناعي الخاص بك.',
        'capabilities': 'يمكنني مساعدتك في:',
        'what_can_i_do': 'كيف تريد أن أساعدك اليوم؟',
        
        'tools_title': 'الأدوات والقدرات',
        'web_search': 'بحث الويب',
        'web_browse': 'متصفح الويب',
        'file_read': 'قراءة الملفات',
        'file_write': 'كتابة الملفات',
        'code_execute': 'تنفيذ الكود',
        'command_run': 'تنفيذ الأوامر',
        
        'security_title': 'أدوات الأمان',
        'port_scan': 'ماسح المنافذ',
        'dns_lookup': 'بحث DNS',
        'whois': 'بحث WHOIS',
        'ssl_analysis': 'تحليل SSL',
        'headers_check': 'رؤوس الأمان',
        'password_check': 'قوة كلمة المرور',
        'hash_identify': 'معرف التجزئة',
        
        'settings_title': 'الإعدادات',
        'language': 'اللغة',
        'voice': 'الصوت',
        'api_key': 'مفتاح API',
        'theme': 'السمة',
        
        'online': 'متصل',
        'offline': 'غير متصل',
        'processing': 'قيد المعالجة',
        
        'error': 'خطأ',
        'success': 'نجاح',
        
        'save': 'حفظ',
        'cancel': 'إلغاء',
        'delete': 'حذف',
        'clear': 'مسح',
        'create': 'إنشاء',
        'rename': 'إعادة تسمية',
    },
    
    'hi': {  # Hindi
        'app_name': 'EVE AI',
        'tagline': 'आपका सार्वभौमिक AI सहायक',
        
        'nav_chat': 'चैट',
        'nav_tools': 'उपकरण',
        'nav_memory': 'मेमोरी',
        'nav_settings': 'सेटिंग्स',
        
        'input_placeholder': 'EVE को संदेश...',
        'send': 'भेजें',
        'thinking': 'सोच रहा है...',
        
        'greeting': 'नमस्ते! मैं EVE हूं, आपका सार्वभौमिक AI सहायक।',
        'capabilities': 'मैं इनमें मदद कर सकता हूं:',
        'what_can_i_do': 'आज मैं आपकी क्या मदद कर सकता हूं?',
        
        'tools_title': 'उपकरण और क्षमताएं',
        'web_search': 'वेब खोज',
        'web_browse': 'वेब ब्राउज़र',
        'file_read': 'फ़ाइलें पढ़ें',
        'file_write': 'फ़ाइलें लिखें',
        'code_execute': 'कोड निष्पादित करें',
        'command_run': 'कमांड चलाएं',
        
        'security_title': 'सुरक्षा उपकरण',
        'port_scan': 'पोर्ट स्कैनर',
        'dns_lookup': 'DNS लुकअप',
        'whois': 'WHOIS लुकअप',
        'ssl_analysis': 'SSL विश्लेषण',
        'headers_check': 'सुरक्षा हेडर',
        'password_check': 'पासवर्ड मजबूती',
        'hash_identify': 'हैश पहचान',
        
        'settings_title': 'सेटिंग्स',
        'language': 'भाषा',
        'voice': 'आवाज़',
        'api_key': 'API कुंजी',
        'theme': 'थीम',
        
        'online': 'ऑनलाइन',
        'offline': 'ऑफ़लाइन',
        'processing': 'प्रोसेसिंग',
        
        'error': 'त्रुटि',
        'success': 'सफलता',
        
        'save': 'सहेजें',
        'cancel': 'रद्द करें',
        'delete': 'हटाएं',
        'clear': 'साफ़ करें',
        'create': 'बनाएं',
        'rename': 'नाम बदलें',
    },
    
    'sw': {  # Swahili
        'app_name': 'EVE AI',
        'tagline': 'Msaidizi wako wa AI',
        
        'nav_chat': 'Mazungumzo',
        'nav_tools': 'Zana',
        'nav_memory': 'Kumbukumbu',
        'nav_settings': 'Mipangilio',
        
        'input_placeholder': 'Ujumbe kwa EVE...',
        'send': 'Tuma',
        'thinking': 'Kufikiria...',
        
        'greeting': 'Habari! Mimi ni EVE, msaidizi wako wa AI.',
        'capabilities': 'Naweza kukusaidia na:',
        'what_can_i_do': 'Ungependa nisaidie nini leo?',
        
        'tools_title': 'Zana na Uwezo',
        'web_search': 'Tafuta Mtandao',
        'web_browse': 'Kivinjari',
        'file_read': 'Soma Faili',
        'file_write': 'Andika Faili',
        'code_execute': 'itekeleza Code',
        'command_run': 'Enda Amri',
        
        'security_title': 'Zana za Usalama',
        'port_scan': 'Kichwa Ports',
        'dns_lookup': 'Tafuta DNS',
        'whois': 'Tafuta WHOIS',
        'ssl_analysis': ' Uchambuzi SSL',
        'headers_check': 'Vichwa Usalama',
        'password_check': 'Nguvu Ya Nywila',
        'hash_identify': ' Tambulisha Hash',
        
        'settings_title': 'Mipangilio',
        'language': 'Lugha',
        'voice': 'Sauti',
        'api_key': 'API Key',
        'theme': 'Mandharinyuma',
        
        'online': 'Mtandaoni',
        'offline': 'Nje ya Mtandao',
        'processing': 'Processing',
        
        'error': 'Hitilafu',
        'success': 'Mafanikio',
        
        'save': 'Hifadhi',
        'cancel': 'Ghairi',
        'delete': 'Futa',
        'clear': 'Futa',
        'create': 'Unda',
        'rename': 'Badilisha Jina',
    },
    
    'zu': {  # Zulu
        'app_name': 'EVE AI',
        'tagline': 'Umphenyi we-AI yakho',
        
        'nav_chat': 'Ingxoxo',
        'nav_tools': 'Izinsiza',
        'nav_memory': 'Imemori',
        'nav_settings': 'Izilungiselelo',
        
        'input_placeholder': 'Umlayezo ku-EVE...',
        'send': 'Thumela',
        'thinking': 'Kucabanga...',
        
        'greeting': 'Sawubona! Ngingu-EVE, umphenyi we-AI yakho.',
        'capabilities': 'Ngingakusiza ngalokhu:',
        'what_can_i_do': 'Ungathanda ngisize ngaki?',
        
        'tools_title': 'Izinsiza namandla',
        'web_search': 'Ukucinga iwebhu',
        'web_browse': 'Iwebhu browser',
        'file_read': 'Funda amafayela',
        'file_write': 'Bhala amafayela',
        'code_execute': 'Qalisa ikhodi',
        'command_run': 'Qalisa imiyalo',
        
        'security_title': 'Izinsiza zokuphepha',
        'port_scan': 'Isikena samapoti',
        'dns_lookup': 'I-DNS lookup',
        'whois': 'I-WHOIS lookup',
        'ssl_analysis': 'I-SSL analysis',
        'headers_check': 'izihloko zokuphepha',
        'password_check': 'Amandla epaswedi',
        'hash_identify': 'Chaza i-hash',
        
        'settings_title': 'Izilungiselelo',
        'language': 'Ulimi',
        'voice': 'Izwi',
        'api_key': 'I-API key',
        'theme': 'Isiteshi',
        
        'online': 'Online',
        'offline': 'Offline',
        'processing': 'Iprocess',
        
        'error': 'Iphutha',
        'success': 'Impumelelo',
        
        'save': 'Gcina',
        'cancel': 'Khansela',
        'delete': 'Susa',
        'clear': 'Sula',
        'create': 'Dala',
        'rename': 'Shintsha igama',
    },
}


class LanguageManager:
    """Manages translations and language settings"""
    
    def __init__(self, default_lang: str = 'en'):
        self.current_language = default_lang
        self.translations = TRANSLATIONS
    
    def set_language(self, lang_code: str) -> bool:
        """Set the current language"""
        if lang_code in self.translations:
            self.current_language = lang_code
            return True
        return False
    
    def get_language(self) -> str:
        """Get current language code"""
        return self.current_language
    
    def t(self, key: str) -> str:
        """Translate a key to current language"""
        translations = self.translations.get(self.current_language, self.translations['en'])
        return translations.get(key, key)
    
    def get_available_languages(self) -> Dict[str, Dict[str, str]]:
        """Get list of available languages"""
        return LANGUAGES
    
    def get_all_translations(self) -> Dict[str, str]:
        """Get all translations for current language"""
        return self.translations.get(self.current_language, self.translations['en'])
    
    def translate_text(self, text: str, target_lang: str) -> str:
        """Translate text to target language (basic)"""
        # This is a placeholder - in production, use a translation API
        if target_lang in self.translations:
            return text  # Return original as placeholder
        return text


# Global language manager
language_manager = LanguageManager()


# Example usage
if __name__ == "__main__":
    lm = language_manager
    
    print("Available languages:")
    for code, info in LANGUAGES.items():
        print(f"  {code}: {info['name']} ({info['native']})")
    
    print("\n--- English ---")
    lm.set_language('en')
    print(f"App name: {lm.t('app_name')}")
    print(f"Greeting: {lm.t('greeting')}")
    
    print("\n--- Japanese ---")
    lm.set_language('ja')
    print(f"App name: {lm.t('app_name')}")
    print(f"Greeting: {lm.t('greeting')}")
    
    print("\n--- Shona ---")
    lm.set_language('sn')
    print(f"App name: {lm.t('app_name')}")
    print(f"Greeting: {lm.t('greeting')}")
    
    print("\n--- Korean ---")
    lm.set_language('ko')
    print(f"App name: {lm.t('app_name')}")
    print(f"Greeting: {lm.t('greeting')}")
    
    print("\n--- Russian ---")
    lm.set_language('ru')
    print(f"App name: {lm.t('app_name')}")
    print(f"Greeting: {lm.t('greeting')}")
