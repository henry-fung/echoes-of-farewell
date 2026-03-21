// ============== i18n Translations ==============
const translations = {
    'zh-CN': {
        // Header
        'logout': '退出',
        // Sidebar
        'profiles': '亲人档案',
        'chat': '对话',
        // Profiles Page
        'my_loved_ones': '我的亲人',
        'profiles_desc': '选择一位亲人开始对话，或添加新的亲人档案',
        'add_loved_one': '添加亲人',
        'no_profiles': '还没有亲人档案',
        'no_profiles_desc': '点击右上角按钮添加第一位亲人',
        'click_to_chat': '点击开始对话',
        'edit': '编辑',
        'delete': '删除',
        // Profile Form
        'add_profile': '添加亲人',
        'edit_profile': '编辑亲人档案',
        'back': '返回',
        'name_required': '姓名 *',
        'name_placeholder': '亲人的名字',
        'personality': '性格描述',
        'personality_placeholder': '例如：温和、幽默、喜欢关心人、说话简洁...',
        'chat_history': '聊天记录',
        'chat_history_placeholder': '粘贴真实的聊天记录，AI 会学习亲人的语言风格、用词习惯、表情使用等...\n\n格式示例：\n亲人：吃饭了吗？\n我：刚吃完\n亲人：多吃点，别饿着',
        'chat_history_hint': '聊天记录越多，AI 模仿得越像',
        'avatar': '头像',
        'avatar_hint': '选择一位亲人的形象',
        'language': '语言',
        'language_hint': '选择亲人常用的语言',
        'gender': '性别',
        'gender_hint': '选择亲人的性别',
        'age': '年龄',
        'age_hint': '选择亲人的年龄段',
        'relationship': '关系',
        'relationship_hint': '选择与您的关系',
        'cancel': '取消',
        'save': '保存',
        'save_success': '保存成功！',
        // Consent Modal
        'consent_title': '用户数据收集知情同意书',
        'consent_read': '我已阅读并理解本同意书的内容',
        'consent_agree': '我自愿同意本服务收集和使用我的数据',
        'consent_withdraw': '我了解我可以随时撤回我的同意',
        'consent_disagree': '不同意并退出',
        'consent_agree_button': '同意并继续',
        // Chat Page
        'select_loved_one': '请先选择一位亲人',
        'select_desc': '从亲人档案中选择一位，开始对话',
        'go_select': '去选择',
        'switch_profile': '切换亲人',
        'online': '在线',
        'clear_history': '清空记录',
        'emotion_state': '情感状态',
        'mood_index': '心情指数',
        'decay_rate': '衰减率',
        'stage': '阶段',
        'recovery_phase': '恢复阶段',
        'memory_weight': '记忆权重',
        'intimacy': '亲密',
        'support': '支持',
        'stability': '稳定度',
        'interactions': '交互次数',
        'next_proactive': '下次主动',
        'safety_alert': '安全警报',
        'stage_distribution': '五阶段分布',
        'denial': '否认',
        'anger': '愤怒',
        'bargaining': '讨价还价',
        'depression': '抑郁',
        'acceptance': '接受',
        'type_message': '想说什么...',
        'send': '发送',
        'clear_confirm': '确定要清空与这位亲人的聊天记录吗？',
        // Chat List Page
        'my_conversations': '我的对话',
        'select_chat_desc': '选择一个亲人继续对话',
        'no_conversations': '暂无对话',
        'no_conversations_desc': '先创建一个亲人档案开始对话吧',
        'tap_to_chat': '点击开始对话',
        // Settings Page
        'settings': '设置',
        'language_settings': '语言设置',
        'about': '关于',
        // Survey Modal
        'survey_title': '情感状态调查问卷',
        'survey_desc': '为了更好地了解您的状态并提供更合适的陪伴，请花几分钟时间回答以下问题。',
        'survey_submit': '提交问卷',
        'survey_q1_title': '1. 今天整体的心情如何？',
        'survey_q1_a1': '非常低落',
        'survey_q1_a2': '有点低落',
        'survey_q1_a3': '平静',
        'survey_q1_a4': '轻微轻松',
        'survey_q1_a5': '明显好转、开心',
        'survey_q2_title': '2. 你现在想起失去的人/宠物/感情时，情绪强度是？',
        'survey_q2_a1': '强烈痛苦、无法控制',
        'survey_q2_a2': '经常难过、影响生活',
        'survey_q2_a3': '偶尔难过，但可以承受',
        'survey_q2_a4': '轻微想念，情绪稳定',
        'survey_q2_a5': '已经能平静面对',
        'survey_q3_title': '3. 你目前更偏向哪种状态？（双过程模型）',
        'survey_q3_a1': '沉浸在回忆与悲伤中',
        'survey_q3_a2': '多数时间难过，偶尔能转移注意力',
        'survey_q3_a3': '悲伤与日常状态各占一半',
        'survey_q3_a4': '更愿意关注生活、向前看',
        'survey_q3_a5': '已回到正常生活节奏',
        'survey_q4_title': '4. 你觉得自己现在处于情绪恢复的哪个阶段？（五阶段模型）',
        'survey_q4_a1': '否认/不愿接受事实',
        'survey_q4_a2': '愤怒/委屈/不甘心',
        'survey_q4_a3': '讨价还价/希望挽回',
        'survey_q4_a4': '低落/空虚/无力',
        'survey_q4_a5': '接受/慢慢放下',
        'survey_q5_title': '5. 你需要我（AI 陪伴者）保持更亲近，还是慢慢淡出？',
        'survey_q5_a1': '需要更亲近陪伴',
        'survey_q5_a2': '保持现在的亲近度就好',
        'survey_q5_a3': '可以稍微慢慢淡出',
        'survey_q5_a4': '可以明显淡出',
        'survey_q5_a5': '已不需要太多陪伴'
    },
    'zh-HK': {
        // Header
        'logout': '退出',
        // Sidebar
        'profiles': '親人檔案',
        'chat': '對話',
        // Profiles Page
        'my_loved_ones': '我嘅親人',
        'profiles_desc': '選擇一位親人開始對話，或添加新嘅親人檔案',
        'add_loved_one': '添加親人',
        'no_profiles': '仲未有親人檔案',
        'no_profiles_desc': '點擊右上角按鈕添加第一位親人',
        'click_to_chat': '點擊開始對話',
        'edit': '編輯',
        'delete': '刪除',
        // Profile Form
        'add_profile': '添加親人',
        'edit_profile': '編輯親人檔案',
        'back': '返回',
        'name_required': '姓名 *',
        'name_placeholder': '親人嘅名',
        'personality': '性格描述',
        'personality_placeholder': '例如：溫和、幽默、鍾意關心人、講說簡潔...',
        'chat_history': '聊天記錄',
        'chat_history_placeholder': '貼上真實嘅聊天記錄，AI 會學習親人嘅語言風格、用詞習慣、表情使用等...\n\n格式示例：\n親人：食飯未？\n我：啱啱食完\n親人：食多啲，唔好餓親',
        'chat_history_hint': '聊天記錄越多，AI 模仿得越似',
        'avatar': '頭像',
        'avatar_hint': '選擇一位親人嘅形象',
        'language': '語言',
        'language_hint': '選擇親人慣用嘅語言',
        'gender': '性別',
        'gender_hint': '選擇親人嘅性別',
        'age': '年齡',
        'age_hint': '選擇親人嘅年齡段',
        'relationship': '關係',
        'relationship_hint': '選擇與您嘅關係',
        'cancel': '取消',
        'save': '保存',
        'save_success': '保存成功！',
        // Consent Modal
        'consent_title': '用戶數據收集知情同意書',
        'consent_read': '我已閱讀並理解本同意書的內容',
        'consent_agree': '我自願同意本服務收集和使用我的數據',
        'consent_withdraw': '我了解我可以隨時撤回我的同意',
        'consent_disagree': '不同意並退出',
        'consent_agree_button': '同意並繼續',
        // Chat Page
        'select_loved_one': '請先選擇一位親人',
        'select_desc': '從親人檔案中選擇一位，開始對話',
        'go_select': '去選擇',
        'switch_profile': '轉換親人',
        'online': '在線',
        'clear_history': '清空記錄',
        'emotion_state': '情感狀態',
        'mood_index': '心情指數',
        'decay_rate': '衰減率',
        'stage': '階段',
        'recovery_phase': '恢復階段',
        'memory_weight': '記憶權重',
        'intimacy': '親密',
        'support': '支持',
        'stability': '穩定度',
        'interactions': '交互次數',
        'next_proactive': '下次主動',
        'safety_alert': '安全警報',
        'stage_distribution': '五階段分佈',
        'denial': '否認',
        'anger': '憤怒',
        'bargaining': '討價還價',
        'depression': '抑郁',
        'acceptance': '接受',
        'type_message': '想講乜...',
        'send': '發送',
        'clear_confirm': '確定要清空同呢位親人嘅聊天記錄嗎？',
        // Survey Modal
        'survey_title': '情感狀態調查問卷',
        'survey_desc': '為了更好地了解您嘅狀態並提供更合適嘅陪伴，請花幾分鐘時間回答以下問題。',
        'survey_submit': '提交問卷',
        'survey_q1_title': '1. 今日整體嘅心情點樣？',
        'survey_q1_a1': '非常低落',
        'survey_q1_a2': '有啲低落',
        'survey_q1_a3': '平靜',
        'survey_q1_a4': '輕微輕鬆',
        'survey_q1_a5': '明顯好轉、開心',
        'survey_q2_title': '2. 你而家諗起失去嘅人/寵物/感情時，情緒強度係？',
        'survey_q2_a1': '強烈痛苦、無法控制',
        'survey_q2_a2': '經常難過、影響生活',
        'survey_q2_a3': '偶爾難過，但可以承受',
        'survey_q2_a4': '輕微想念，情緒穩定',
        'survey_q2_a5': '已經能平靜面對',
        'survey_q3_title': '3. 你目前更偏向哪種狀態？（雙過程模型）',
        'survey_q3_a1': '沉浸喺回憶與悲傷中',
        'survey_q3_a2': '多數時間難過，偶爾能轉移注意力',
        'survey_q3_a3': '悲傷與日常狀態各佔一半',
        'survey_q3_a4': '更願意關注生活、向前看',
        'survey_q3_a5': '已回到正常生活節奏',
        'survey_q4_title': '4. 你覺得自己而家處於情緒恢復嘅哪個階段？（五階段模型）',
        'survey_q4_a1': '否認/不願接受事實',
        'survey_q4_a2': '憤怒/委屈/不甘心',
        'survey_q4_a3': '討價還價/希望挽回',
        'survey_q4_a4': '低落/空虛/無力',
        'survey_q4_a5': '接受/慢慢放下',
        'survey_q5_title': '5. 你需要我（AI 陪伴者）保持更親近，定係慢慢淡出？',
        'survey_q5_a1': '需要更親近陪伴',
        'survey_q5_a2': '保持而家嘅親近度就好',
        'survey_q5_a3': '可以稍微慢慢淡出',
        'survey_q5_a4': '可以明顯淡出',
        'survey_q5_a5': '已不需要太多陪伴'
    },
    'en': {
        // Header
        'logout': 'Logout',
        // Sidebar
        'profiles': 'Loved Ones',
        'chat': 'Chat',
        // Profiles Page
        'my_loved_ones': 'My Loved Ones',
        'profiles_desc': 'Select a loved one to chat with, or add a new profile',
        'add_loved_one': 'Add Loved One',
        'no_profiles': 'No profiles yet',
        'no_profiles_desc': 'Click the button above to add your first loved one',
        'click_to_chat': 'Click to start chatting',
        'edit': 'Edit',
        'delete': 'Delete',
        // Profile Form
        'add_profile': 'Add Loved One',
        'edit_profile': 'Edit Profile',
        'back': 'Back',
        'name_required': 'Name *',
        'name_placeholder': 'Name of your loved one',
        'personality': 'Personality',
        'personality_placeholder': 'e.g., gentle, humorous, caring, concise...',
        'chat_history': 'Chat History',
        'chat_history_placeholder': 'Paste real chat history for AI to learn their language style, vocabulary, and expression habits...\n\nFormat example:\nLoved One: Have you eaten?\nMe: Just finished\nLoved One: Eat more, don\'t starve',
        'chat_history_hint': 'More chat history helps AI mimic better',
        'avatar': 'Avatar',
        'avatar_hint': 'Choose an image representing your loved one',
        'language': 'Language',
        'language_hint': 'Select the language your loved one commonly used',
        'cancel': 'Cancel',
        'save': 'Save',
        'save_success': 'Saved successfully!',
        // Consent Modal
        'consent_title': 'Informed Consent Form for User Data Collection',
        'consent_read': 'I have read and understood the content of this consent form',
        'consent_agree': 'I voluntarily consent to the Service collecting and using my data',
        'consent_withdraw': 'I understand that I can withdraw my consent at any time',
        'consent_disagree': 'Disagree and Logout',
        'consent_agree_button': 'Agree and Continue',
        // Chat Page
        'select_loved_one': 'Please select a loved one first',
        'select_desc': 'Choose from your profiles to start a conversation',
        'go_select': 'Go Select',
        'switch_profile': 'Switch',
        'online': 'Online',
        'clear_history': 'Clear History',
        'emotion_state': 'Emotion State',
        'mood_index': 'Mood Index',
        'decay_rate': 'Decay Rate',
        'stage': 'Stage',
        'recovery_phase': 'Recovery Phase',
        'memory_weight': 'Memory Weight',
        'intimacy': 'Intimacy',
        'support': 'Support',
        'stability': 'Stability',
        'interactions': 'Interactions',
        'next_proactive': 'Next Proactive',
        'safety_alert': 'Safety Alert',
        'stage_distribution': 'Stage Distribution',
        'denial': 'Denial',
        'anger': 'Anger',
        'bargaining': 'Bargaining',
        'depression': 'Depression',
        'acceptance': 'Acceptance',
        'type_message': 'Type a message...',
        'send': 'Send',
        'clear_confirm': 'Are you sure you want to clear the chat history with this loved one?',
        // Survey Modal
        'survey_title': 'Emotional State Survey',
        'survey_desc': 'To better understand your condition and provide more suitable companionship, please take a few minutes to answer the following questions.',
        'survey_submit': 'Submit Survey',
        'survey_q1_title': '1. How is your overall mood today?',
        'survey_q1_a1': 'Very low',
        'survey_q1_a2': 'Somewhat low',
        'survey_q1_a3': 'Calm',
        'survey_q1_a4': 'Slightly relieved',
        'survey_q1_a5': 'Significantly better, happy',
        'survey_q2_title': '2. When you think about the person/pet/relationship you lost, what is your emotional intensity?',
        'survey_q2_a1': 'Intense pain, uncontrollable',
        'survey_q2_a2': 'Frequently sad, affecting daily life',
        'survey_q2_a3': 'Occasionally sad, but manageable',
        'survey_q2_a4': 'Slight longing, emotionally stable',
        'survey_q2_a5': 'Can face it calmly now',
        'survey_q3_title': '3. Which state are you currently leaning towards? (Dual Process Model)',
        'survey_q3_a1': 'Immersed in memories and sadness',
        'survey_q3_a2': 'Mostly sad, occasionally able to distract',
        'survey_q3_a3': 'Half sadness, half daily life',
        'survey_q3_a4': 'More willing to focus on life, move forward',
        'survey_q3_a5': 'Back to normal life rhythm',
        'survey_q4_title': '4. Which stage of emotional recovery do you feel you are in? (Five Stages Model)',
        'survey_q4_a1': 'Denial / Unwilling to accept reality',
        'survey_q4_a2': 'Anger / Grievance / Unreconciled',
        'survey_q4_a3': 'Bargaining / Hoping to recover',
        'survey_q4_a4': 'Depression / Emptiness / Powerless',
        'survey_q4_a5': 'Acceptance / Letting go slowly',
        'survey_q5_title': '5. Do you need me (AI companion) to stay closer or fade out slowly?',
        'survey_q5_a1': 'Need closer companionship',
        'survey_q5_a2': 'Current intimacy level is fine',
        'survey_q5_a3': 'Can fade out slowly',
        'survey_q5_a4': 'Can fade out significantly',
        'survey_q5_a5': 'Don\'t need much companionship anymore'
    }
};

// 根据浏览器语言设置默认 UI 语言
function getBrowserLanguage() {
    const browserLang = navigator.language || navigator.userLanguage;
    const lang = browserLang.toLowerCase();

    if (lang.startsWith('zh-cn') || lang.startsWith('zh-sg')) {
        return 'zh-CN';
    } else if (lang.startsWith('zh-hk') || lang.startsWith('zh-hant')) {
        return 'zh-HK';
    } else if (lang.startsWith('zh-tw') || lang.startsWith('zh-hant')) {
        return 'zh-HK';
    } else {
        return 'en'; // Default to English for other languages
    }
}

let currentUILanguage = localStorage.getItem('uiLanguage') || getBrowserLanguage();

function changeUILanguage(lang) {
    currentUILanguage = lang;
    localStorage.setItem('uiLanguage', lang);

    // Sync all language selectors
    const mainSelector = document.getElementById('uiLanguage');
    const consentSelector = document.getElementById('consentLanguage');
    const surveySelector = document.getElementById('surveyLanguage');
    if (mainSelector) mainSelector.value = lang;
    if (consentSelector) consentSelector.value = lang;
    if (surveySelector) surveySelector.value = lang;

    updateAllUIText();

    // Update consent modal content if visible
    if (!document.getElementById('consentModal').classList.contains('hidden')) {
        loadConsentContent();
    }
}

function t(key) {
    return translations[currentUILanguage]?.[key] || translations['zh-CN'][key] || key;
}

function updateAllUIText() {
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (key) {
            el.textContent = t(key);
        }
    });
    
    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (key) {
            el.placeholder = t(key);
        }
    });
}

// ============== State Management ==============
const state = {
    token: localStorage.getItem('token'),
    user: null,
    profiles: [],
    currentProfile: null,  // Currently selected profile for chat
    currentProfileId: parseInt(sessionStorage.getItem('currentProfileId')) || null,
    currentPage: 'profiles',
    isLoading: false,
    hasConfirmedConsentThisSession: false,  // Track if user confirmed consent in current session
    surveyDue: false,  // Track if survey is due (every 5 days)
    lastSurveyDate: null  // Last survey submission date
};

// ============== API Functions ==============
const API_BASE = '';

async function api(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const isFormData = options.body instanceof FormData;
    
    // 设置默认超时为60秒（LLM生成需要时间）
    const timeout = options.timeout || 60000;
    
    const config = {
        headers: {
            ...(!isFormData && { 'Content-Type': 'application/json' }),
            ...options.headers
        },
        ...options
    };
    
    if (state.token) {
        config.headers['Authorization'] = `Bearer ${state.token}`;
    }
    
    if (config.body && typeof config.body === 'object' && !isFormData) {
        config.body = JSON.stringify(config.body);
    }
    
    // 创建 AbortController 用于超时控制
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
        config.signal = controller.signal;
        const response = await fetch(url, config);
        clearTimeout(timeoutId);
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || '请求失败');
        }
        
        return data;
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('请求超时，请稍后再试');
        }
        throw error;
    }
}

// ============== Auth Functions ==============

async function login(username, password) {
    return api('/api/login', {
        method: 'POST',
        body: { username, password }
    });
}

async function register(username, password, inviteCode) {
    return api('/api/register', {
        method: 'POST',
        body: { username, password, invite_code: inviteCode }
    });
}

async function getMe() {
    return api('/api/me');
}

// ============== Consent Functions ==============

async function getConsent() {
    return api('/api/consent');
}

async function updateConsent(consent_given) {
    return api('/api/consent', {
        method: 'POST',
        body: { consent_given }
    });
}

// ============== Survey Functions ==============

async function getSurveyStatus() {
    return api('/api/survey/status');
}

async function submitSurveyData(answers) {
    return api('/api/survey/submit', {
        method: 'POST',
        body: { answers }
    });
}

// ============== Profile Functions ==============

async function getProfiles() {
    return api('/api/profiles');
}

async function getProfile(profileId) {
    return api(`/api/profiles/${profileId}`);
}

async function createProfile(formData) {
    return api('/api/profiles', {
        method: 'POST',
        body: formData
    });
}

async function updateProfile(profileId, formData) {
    return api(`/api/profiles/${profileId}`, {
        method: 'PUT',
        body: formData
    });
}

async function deleteProfile(profileId) {
    return api(`/api/profiles/${profileId}`, {
        method: 'DELETE'
    });
}

// ============== Client Context Functions ==============

// Cache for client context to avoid repeated geolocation requests
let cachedContext = null;
let contextCacheTime = 0;
const CONTEXT_CACHE_DURATION = 60000;  // 1 minute cache

// Get client context (time, location, weather) for LLM responses
async function getClientContext() {
    const now = Date.now();
    
    // Return cached context if still valid (for rapid successive requests)
    if (cachedContext && (now - contextCacheTime) < CONTEXT_CACHE_DURATION) {
        // Update timestamp for accurate time
        return {
            ...cachedContext,
            client_timestamp: new Date().toISOString()
        };
    }
    
    const context = {
        client_timestamp: new Date().toISOString(),
        client_timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
    };
    
    console.log('[Client Context] Timezone:', context.client_timezone);
    
    // Try to get location from browser Geolocation API
    try {
        const position = await getCurrentPosition();
        if (position) {
            context.client_lat = position.coords.latitude;
            context.client_lon = position.coords.longitude;
            console.log('[Client Context] Got location:', context.client_lat, context.client_lon);
        }
    } catch (err) {
        console.log('[Client Context] Location not available:', err.message);
    }
    
    // Cache the context (without timestamp)
    cachedContext = {
        client_timezone: context.client_timezone,
        client_lat: context.client_lat,
        client_lon: context.client_lon
    };
    contextCacheTime = now;
    
    return context;
}

// Promise wrapper for geolocation API with faster timeout
function getCurrentPosition() {
    return new Promise((resolve) => {
        if (!navigator.geolocation) {
            console.log('[Geolocation] Not supported');
            resolve(null);
            return;
        }
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                console.log('[Geolocation] Success');
                resolve(position);
            },
            (error) => {
                const errorMessages = {
                    1: '用户拒绝授权',
                    2: '位置服务不可用',
                    3: '获取位置超时'
                };
                console.log('[Geolocation] Error:', errorMessages[error.code] || error.message);
                resolve(null);  // Resolve with null instead of rejecting to not block chat
            },
            {
                enableHighAccuracy: false,
                timeout: 3000,  // Faster timeout
                maximumAge: 300000  // 5 minutes cache
            }
        );
    });
}

// ============== Chat Functions ==============

async function sendChatMessage(profileId, message) {
    // LLM 生成需要较长时间，使用 90 秒超时
    // Get client context for time/location/weather-based responses
    const clientContext = await getClientContext();
    
    return api('/api/chat', {
        method: 'POST',
        body: {
            profile_id: profileId,
            message,
            ...clientContext
        },
        timeout: 90000  // 90 秒
    });
}

async function getChatHistory(profileId) {
    return api(`/api/chat/history?profile_id=${profileId}`);
}

async function clearChatHistory(profileId) {
    return api(`/api/chat/history?profile_id=${profileId}`, {
        method: 'DELETE'
    });
}

// ============== UI Functions ==============

function showLoading() {
    document.getElementById('loadingOverlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.add('hidden');
}

function showError(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = message;
        setTimeout(() => {
            el.textContent = '';
        }, 5000);
    }
}

function switchTab(tab) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const tabs = document.querySelectorAll('.tab-btn');
    
    tabs.forEach(t => t.classList.remove('active'));
    
    if (tab === 'login') {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        tabs[0].classList.add('active');
    } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        tabs[1].classList.add('active');
    }
}

function showPage(page) {
    state.currentPage = page;
    // Save last visited page for restoration after refresh
    if (page === 'chat' || page === 'profiles') {
        sessionStorage.setItem('lastPage', page);
    }
    
    // Update nav - 只有"亲人档案"是导航项，对话列表单独处理
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    if (page === 'profiles' || page === 'profileForm') {
        document.getElementById('navProfiles').classList.add('active');
    }
    
    // Hide all pages
    document.getElementById('profilesPage').classList.add('hidden');
    document.getElementById('profileFormPage').classList.add('hidden');
    document.getElementById('chatPage').classList.add('hidden');
    
    // Show requested page
    document.getElementById(`${page}Page`).classList.remove('hidden');
    
    // Page specific logic
    if (page === 'profiles') {
        loadProfiles();
    } else if (page === 'chat') {
        // 如果没有选中亲人，默认选中第一个
        if (!state.currentProfile && state.profiles.length > 0) {
            state.currentProfile = state.profiles[0];
        }
        loadChat();
    }
}

// ============== Auth Handlers ==============

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        showLoading();
        const data = await login(username, password);
        state.token = data.token;
        state.user = { username: data.username };
        localStorage.setItem('token', data.token);

        // Initialize UI language before showing consent
        document.getElementById('uiLanguage').value = currentUILanguage;
        updateAllUIText();

        // Always show consent modal on login for re-confirmation
        // Hide auth modal and show consent modal
        document.getElementById('authModal').classList.add('hidden');
        showConsentModal();
    } catch (err) {
        showError('loginError', err.message);
    } finally {
        hideLoading();
    }
});

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    const inviteCode = document.getElementById('inviteCode').value;

    try {
        showLoading();
        const data = await register(username, password, inviteCode);
        state.token = data.token;
        state.user = { username: data.username };
        localStorage.setItem('token', data.token);

        // Initialize UI language before showing consent
        document.getElementById('uiLanguage').value = currentUILanguage;
        updateAllUIText();

        // New users need to give consent
        document.getElementById('authModal').classList.add('hidden');
        showConsentModal();
    } catch (err) {
        showError('registerError', err.message);
    } finally {
        hideLoading();
    }
});

function logout() {
    state.token = null;
    state.user = null;
    state.profiles = [];
    state.currentProfile = null;
    state.currentProfileId = null;
    state.hasConfirmedConsentThisSession = false;
    localStorage.removeItem('token');
    sessionStorage.clear();
    document.getElementById('authModal').classList.remove('hidden');
    document.getElementById('app').classList.add('hidden');
}

// ============== Profile Handlers ==============

function showCreateProfileForm() {
    // Reset form
    document.getElementById('profileForm').reset();
    document.getElementById('editProfileId').value = '';
    document.getElementById('profileFormTitle').textContent = '添加亲人';
    document.getElementById('profileSuccess').textContent = '';

    // Reset relationship
    document.getElementById('profileRelationship').value = '';
    document.getElementById('customRelationship').value = '';
    document.getElementById('customRelationship').classList.add('hidden');

    // Reset avatar selection
    document.querySelectorAll('.avatar-option').forEach(opt => opt.classList.remove('selected'));
    document.getElementById('selectedAvatar').value = '';
    document.getElementById('customPhotoPreview').classList.add('hidden');
    document.getElementById('customPhotoImg').src = '';

    // Reset image upload status
    hideExtractStatus();
    const imageInput = document.getElementById('chatImageUpload');
    if (imageInput) imageInput.value = '';

    // Select grandpa avatar by default
    selectAvatar(document.querySelector('.avatar-option[data-avatar="/static/avatars/grandpa.svg"]'));

    // Reset language to zh-CN (default)
    const defaultLang = document.querySelector('input[name="language"][value="zh-CN"]');
    if (defaultLang) defaultLang.checked = true;

    // Reset gender and age (default to male and middle-aged)
    const defaultGender = document.querySelector('input[name="gender"][value="male"]');
    if (defaultGender) defaultGender.checked = true;
    const defaultAge = document.querySelector('input[name="age"][value="middle"]');
    if (defaultAge) defaultAge.checked = true;

    // Filter relationships based on default gender/age
    filterRelationshipsByGender();

    showPage('profileForm');
}

function showEditProfileForm(profileId) {
    const profile = state.profiles.find(p => p.id === profileId);
    if (!profile) return;
    
    document.getElementById('editProfileId').value = profileId;
    document.getElementById('profileName').value = profile.name || '';
    document.getElementById('profilePersonality').value = profile.personality || '';
    document.getElementById('profileChatHistory').value = profile.chat_history_text || '';
    document.getElementById('profileFormTitle').textContent = '编辑亲人档案';
    document.getElementById('profileSuccess').textContent = '';
    
    // Reset avatar selection
    document.querySelectorAll('.avatar-option').forEach(opt => opt.classList.remove('selected'));
    document.getElementById('selectedAvatar').value = '';
    document.getElementById('customPhotoPreview').classList.add('hidden');
    document.getElementById('customPhotoImg').src = '';
    
    // Reset image upload status
    hideExtractStatus();
    const imageInput = document.getElementById('chatImageUpload');
    if (imageInput) imageInput.value = '';
    
    // Set avatar or photo
    if (profile.photo_path) {
        if (profile.photo_path.includes('/avatars/avatar')) {
            // Built-in avatar
            const avatarOption = document.querySelector(`.avatar-option[data-avatar="${profile.photo_path}"]`);
            if (avatarOption) {
                selectAvatar(avatarOption);
            }
        } else {
            // Custom photo
            document.getElementById('customPhotoImg').src = profile.photo_path;
            document.getElementById('customPhotoPreview').classList.remove('hidden');
        }
    } else {
        // Select first avatar as default
        selectAvatar(document.querySelector('.avatar-option[data-avatar]'));
    }
    
    // Set language
    if (profile.language) {
        const langRadio = document.querySelector(`input[name="language"][value="${profile.language}"]`);
        if (langRadio) {
            langRadio.checked = true;
        } else {
            // Fallback to zh-CN
            const defaultLang = document.querySelector('input[name="language"][value="zh-CN"]');
            if (defaultLang) defaultLang.checked = true;
        }
    }

    // Set gender
    if (profile.gender) {
        const genderRadio = document.querySelector(`input[name="gender"][value="${profile.gender}"]`);
        if (genderRadio) {
            genderRadio.checked = true;
        }
    }

    // Set age
    if (profile.age) {
        const ageRadio = document.querySelector(`input[name="age"][value="${profile.age}"]`);
        if (ageRadio) {
            ageRadio.checked = true;
        }
    }

    // Set relationship
    if (profile.relationship) {
        setRelationshipValue(profile.relationship);
    }

    // Filter relationships based on current gender/age
    filterRelationshipsByGender();

    showPage('profileForm');
}

// ============== Relationship Handler ==============
function handleRelationshipChange(select) {
    const customInput = document.getElementById('customRelationship');
    if (select.value === 'custom') {
        customInput.classList.remove('hidden');
        customInput.focus();
    } else {
        customInput.classList.add('hidden');
        customInput.value = '';
    }
}

// Filter relationships based on selected gender and age
function filterRelationshipsByGender() {
    const genderRadios = document.querySelectorAll('input[name="gender"]');
    const ageRadios = document.querySelectorAll('input[name="age"]');
    const select = document.getElementById('profileRelationship');

    let selectedGender = null;
    let selectedAge = null;

    genderRadios.forEach(radio => {
        if (radio.checked) selectedGender = radio.value;
    });

    ageRadios.forEach(radio => {
        if (radio.checked) selectedAge = radio.value;
    });

    // If no gender selected, show all
    if (!selectedGender && !selectedAge) {
        Array.from(select.options).forEach(opt => {
            opt.disabled = false;
        });
        Array.from(select.querySelectorAll('optgroup')).forEach(optgroup => {
            optgroup.disabled = false;
            optgroup.style.display = '';
        });
        select.querySelector('option[value=""]').textContent = '请选择关系...';
        return;
    }

    // Update select placeholder
    const placeholder = select.querySelector('option[value=""]');
    if (placeholder) {
        placeholder.textContent = '请选择匹配的关系...';
    }

    // Filter options
    Array.from(select.options).forEach(opt => {
        if (!opt.value || opt.value === 'custom') {
            opt.disabled = false;
            return;
        }

        const optGender = opt.getAttribute('data-gender');
        const optAge = opt.getAttribute('data-age');

        // Check if option matches selected gender
        const genderMatch = !selectedGender || optGender === selectedGender;

        // Check if option matches selected age (only for non-pet)
        const ageMatch = !selectedAge || selectedGender === 'pet' || optAge === selectedAge || optAge === null;

        // Pets are always shown if gender is pet
        const isPet = selectedGender === 'pet' && (opt.value === 'cat' || opt.value === 'dog');

        opt.disabled = !(genderMatch && (ageMatch || isPet));
    });

    // Hide empty optgroups
    const optgroups = select.querySelectorAll('optgroup');
    for (let i = 0; i < optgroups.length; i++) {
        const optgroup = optgroups[i];
        const options = optgroup.options || optgroup.querySelectorAll('option');
        let hasVisible = false;
        for (let j = 0; j < options.length; j++) {
            if (!options[j].disabled) {
                hasVisible = true;
                break;
            }
        }
        if (!hasVisible && optgroup.className !== 'rel-other') {
            optgroup.disabled = true;
        } else {
            optgroup.disabled = false;
        }
    }

    // Reset current selection if it's now disabled
    if (select.value && select.selectedOptions[0] && select.selectedOptions[0].disabled) {
        select.value = '';
    }
}

// Get relationship value (including custom)
function getRelationshipValue() {
    const select = document.getElementById('profileRelationship');
    const customInput = document.getElementById('customRelationship');
    if (select.value === 'custom' && customInput.value.trim()) {
        return customInput.value.trim();
    }
    return select.value;
}

// Set relationship value when editing
function setRelationshipValue(value) {
    if (!value) return;

    const select = document.getElementById('profileRelationship');
    const customInput = document.getElementById('customRelationship');

    // Check if value matches an option
    const optionExists = Array.from(select.options).some(opt => opt.value === value);
    if (optionExists) {
        select.value = value;
        customInput.classList.add('hidden');
        customInput.value = '';
    } else {
        // Custom value
        select.value = 'custom';
        customInput.classList.remove('hidden');
        customInput.value = value;
    }
}

function selectAvatar(element) {
    // Remove selection from all options
    document.querySelectorAll('.avatar-option').forEach(opt => opt.classList.remove('selected'));

    // Add selection to clicked option
    element.classList.add('selected');

    // Store selected avatar path
    const avatarPath = element.getAttribute('data-avatar');
    if (avatarPath) {
        document.getElementById('selectedAvatar').value = avatarPath;
        // Hide custom photo if any
        document.getElementById('customPhotoPreview').classList.add('hidden');
    }
}

function previewCustomPhoto(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        // Remove selection from built-in avatars
        document.querySelectorAll('.avatar-option').forEach(opt => opt.classList.remove('selected'));
        
        // Show custom photo preview
        document.getElementById('customPhotoImg').src = e.target.result;
        document.getElementById('customPhotoPreview').classList.remove('hidden');
        document.getElementById('selectedAvatar').value = '';
    };
    reader.readAsDataURL(file);
}

function removeCustomPhoto() {
    document.getElementById('profilePhoto').value = '';
    document.getElementById('customPhotoPreview').classList.add('hidden');
    document.getElementById('customPhotoImg').src = '';
    
    // Select first avatar as default
    selectAvatar(document.querySelector('.avatar-option[data-avatar]'));
}

// ============== Chat History Image Extraction ==============

// Handle multiple images upload for chat history extraction
async function uploadChatImages(input) {
    console.log('[Image Upload] Starting upload, files:', input.files);
    
    const files = Array.from(input.files);
    if (files.length === 0) {
        console.log('[Image Upload] No files selected');
        return;
    }
    
    // Check authentication
    if (!state.token) {
        showExtractStatus('请先登录后再上传图片', 'error');
        return;
    }
    
    console.log(`[Image Upload] Processing ${files.length} files`);
    
    // Validate all files
    for (const file of files) {
        console.log(`[Image Upload] Validating file: ${file.name}, type: ${file.type}, size: ${file.size}`);
        if (!file.type.startsWith('image/')) {
            showExtractStatus(`文件 "${file.name}" 不是图片格式`, 'error');
            input.value = '';
            return;
        }
        if (file.size > 10 * 1024 * 1024) {
            showExtractStatus(`文件 "${file.name}" 超过10MB限制`, 'error');
            input.value = '';
            return;
        }
    }
    
    // Get selected language
    const languageRadio = document.querySelector('input[name="language"]:checked');
    const language = languageRadio ? languageRadio.value : 'zh-CN';
    
    const chatHistoryArea = document.getElementById('profileChatHistory');
    let successCount = 0;
    let failCount = 0;
    let totalChars = 0;
    
    // Process images sequentially to maintain order
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        showExtractStatus(`正在处理第 ${i + 1}/${files.length} 张图片: ${file.name}...`, 'processing');
        
        try {
            const formData = new FormData();
            formData.append('image', file);
            formData.append('language', language);
            
            console.log(`[Image Upload] Sending request for ${file.name}`);
            
            const response = await fetch('/api/extract-chat-from-image', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${state.token}`
                },
                body: formData
            });
            
            console.log(`[Image Upload] Response status: ${response.status}`);
            
            const data = await response.json();
            console.log(`[Image Upload] Response data:`, data);
            
            if (!response.ok) {
                throw new Error(data.detail || `图片识别失败 (HTTP ${response.status})`);
            }
            
            if (data.success && data.extracted_text) {
                const currentText = chatHistoryArea.value;
                const separator = files.length > 1 
                    ? '\n\n' + '='.repeat(20) + ` 图片 ${i + 1} ` + '='.repeat(20) + '\n\n'
                    : '\n\n';
                
                if (currentText && !currentText.endsWith('\n')) {
                    chatHistoryArea.value = currentText + separator + data.extracted_text;
                } else if (currentText) {
                    chatHistoryArea.value = currentText + separator + data.extracted_text;
                } else {
                    chatHistoryArea.value = data.extracted_text;
                }
                
                successCount++;
                totalChars += data.extracted_text.length;
                console.log(`[Image Upload] Success for ${file.name}, extracted ${data.extracted_text.length} chars`);
            } else {
                failCount++;
                console.warn(`[Image Upload] No text extracted from ${file.name}`);
            }
        } catch (err) {
            console.error(`[Image Upload] Error for ${file.name}:`, err);
            showExtractStatus(`处理失败: ${err.message}`, 'error');
            failCount++;
            // Wait a bit before continuing to next image
            await new Promise(r => setTimeout(r, 500));
        }
    }
    
    // Show final status
    if (successCount === files.length && successCount > 0) {
        showExtractStatus(`✅ 全部成功！共处理 ${successCount} 张图片，提取约 ${totalChars} 字符`, 'success');
    } else if (successCount > 0) {
        showExtractStatus(`⚠️ 部分成功：${successCount} 张成功，${failCount} 张失败，共提取约 ${totalChars} 字符`, 'success');
    } else {
        showExtractStatus('❌ 所有图片处理失败，请检查图片内容或网络连接', 'error');
    }
    
    // Clear status after 8 seconds
    setTimeout(() => {
        hideExtractStatus();
    }, 8000);
    
    // Reset file input
    input.value = '';
}

// Show extraction status message
function showExtractStatus(message, type) {
    const statusEl = document.getElementById('imageExtractStatus');
    statusEl.textContent = message;
    statusEl.className = `extract-status ${type}`;
    statusEl.classList.remove('hidden');
}

// Hide extraction status
function hideExtractStatus() {
    const statusEl = document.getElementById('imageExtractStatus');
    statusEl.classList.add('hidden');
}

// Test function for debugging
function testImageUpload() {
    console.log('[Test] state.token:', state.token ? '存在' : '不存在');
    console.log('[Test] imageExtractStatus element:', document.getElementById('imageExtractStatus'));
    console.log('[Test] profileChatHistory element:', document.getElementById('profileChatHistory'));
    console.log('[Test] chatImageUpload element:', document.getElementById('chatImageUpload'));
    
    showExtractStatus('测试提示：功能正常', 'success');
    setTimeout(hideExtractStatus, 3000);
}

document.getElementById('profileForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const profileId = document.getElementById('editProfileId').value;
    const formData = new FormData();
    formData.append('name', document.getElementById('profileName').value);
    formData.append('personality', document.getElementById('profilePersonality').value);
    formData.append('chat_history_text', document.getElementById('profileChatHistory').value);

    // Get gender
    const genderRadio = document.querySelector('input[name="gender"]:checked');
    if (genderRadio) {
        formData.append('gender', genderRadio.value);
    }

    // Get age
    const ageRadio = document.querySelector('input[name="age"]:checked');
    if (ageRadio) {
        formData.append('age', ageRadio.value);
    }

    // Get relationship value
    const relationship = getRelationshipValue();
    if (relationship) {
        formData.append('relationship', relationship);
    }

    // Get selected language
    const languageRadio = document.querySelector('input[name="language"]:checked');
    if (languageRadio) {
        formData.append('language', languageRadio.value);
    }
    
    // Handle avatar/photo
    const photoFile = document.getElementById('profilePhoto').files[0];
    const selectedAvatar = document.getElementById('selectedAvatar').value;
    
    if (photoFile) {
        // Custom photo uploaded
        formData.append('photo', photoFile);
    } else if (selectedAvatar) {
        // Built-in avatar selected - send the path
        formData.append('avatar_path', selectedAvatar);
    }
    
    try {
        showLoading();
        if (profileId) {
            await updateProfile(profileId, formData);
        } else {
            await createProfile(formData);
        }
        document.getElementById('profileSuccess').textContent = '保存成功！';
        setTimeout(() => {
            showPage('profiles');
        }, 1000);
    } catch (err) {
        alert('保存失败: ' + err.message);
    } finally {
        hideLoading();
    }
});

async function handleDeleteProfile(profileId, event) {
    event.stopPropagation();
    
    if (!confirm('确定要删除这位亲人的档案吗？聊天记录也会被删除。')) {
        return;
    }
    
    try {
        showLoading();
        await deleteProfile(profileId);
        // Clear current profile if it was deleted
        if (state.currentProfile && state.currentProfile.id === profileId) {
            state.currentProfile = null;
        }
        await loadProfiles();
    } catch (err) {
        alert('删除失败: ' + err.message);
    } finally {
        hideLoading();
    }
}

async function loadProfiles() {
    try {
        const data = await getProfiles();
        state.profiles = data.profiles || [];
        renderProfilesList();
        renderChatProfilesList(); // 更新侧边栏对话列表
    } catch (err) {
        console.error('Failed to load profiles:', err);
        state.profiles = [];
        renderProfilesList();
        renderChatProfilesList();
    }
}

// 渲染侧边栏对话列表
function renderChatProfilesList() {
    const container = document.getElementById('chatProfilesList');
    
    if (state.profiles.length === 0) {
        container.innerHTML = `
            <button class="chat-profile-item empty" onclick="showPage('profiles')">
                <span>+</span>
                <span class="chat-profile-name">${t('add_loved_one')}</span>
            </button>
        `;
        return;
    }
    
    container.innerHTML = state.profiles.map(profile => `
        <button class="chat-profile-item ${state.currentProfile?.id === profile.id ? 'active' : ''}" 
                onclick="selectProfileAndChat(${profile.id})">
            <img src="${profile.photo_path || 'data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle cx=\"50\" cy=\"50\" r=\"50\" fill=\"%23e0e7ff\"/><text x=\"50\" y=\"60\" text-anchor=\"middle\" font-size=\"40\" fill=\"%236366f1\">👤</text></svg>'}" 
                 alt="${profile.name}" class="chat-profile-avatar">
            <span class="chat-profile-name">${profile.name}</span>
        </button>
    `).join('');
}

// 选择亲人并进入聊天
function selectProfileAndChat(profileId) {
    const profile = state.profiles.find(p => p.id === profileId);
    if (profile) {
        state.currentProfile = profile;
        state.currentProfileId = profileId;
        sessionStorage.setItem('currentProfileId', profileId);
        renderChatProfilesList(); // 更新选中状态
        showPage('chat');
    }
}

function renderProfilesList() {
    const container = document.getElementById('profilesList');
    
    if (state.profiles.length === 0) {
        container.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1; padding: 3rem;">
                <div class="empty-icon">📝</div>
                <h3>还没有亲人档案</h3>
                <p>点击右上角按钮添加第一位亲人</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = state.profiles.map(profile => `
        <div class="profile-card" onclick="selectProfileForChat(${profile.id})">
            <img src="${profile.photo_path || 'data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle cx=\"50\" cy=\"50\" r=\"50\" fill=\"%23e0e7ff\"/><text x=\"50\" y=\"60\" text-anchor=\"middle\" font-size=\"40\" fill=\"%236366f1\">👤</text></svg>'}" 
                 alt="${profile.name}" class="profile-card-avatar">
            <div class="profile-card-name">${profile.name}</div>
            <div class="profile-card-hint">点击开始对话</div>
            <div class="profile-card-actions">
                <button class="btn-small btn-edit" onclick="showEditProfileForm(${profile.id}); event.stopPropagation();">编辑</button>
                <button class="btn-small btn-delete" onclick="handleDeleteProfile(${profile.id}, event)">删除</button>
            </div>
        </div>
    `).join('');
}

function selectProfileForChat(profileId) {
    const profile = state.profiles.find(p => p.id === profileId);
    if (profile) {
        state.currentProfile = profile;
        state.currentProfileId = profileId;
        sessionStorage.setItem('currentProfileId', profileId);
        showPage('chat');
    }
}

// ============== Emotion Panel Functions ==============

function toggleEmotionPanel() {
    const panel = document.getElementById('emotionPanel');
    panel.classList.toggle('hidden');
    if (!panel.classList.contains('hidden') && state.currentProfile) {
        loadEmotionState();
    }
}

async function loadEmotionState() {
    if (!state.currentProfile) return;
    
    try {
        const response = await fetch(`/api/emotion/state?profile_id=${state.currentProfile.id}`, {
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        const data = await response.json();
        
        if (data.success) {
            updateEmotionPanel(data.emotion_state);
        }
    } catch (err) {
        console.error('Failed to load emotion state:', err);
    }
}

function updateEmotionPanel(emotion) {
    // 心情指数
    document.getElementById('moodBarFill').style.width = `${emotion.mood_index}%`;
    document.getElementById('moodValue').textContent = `${emotion.mood_index}/100`;
    
    // 衰减率
    document.getElementById('decayRate').textContent = emotion.decay_rate.toFixed(4);
    
    // 五阶段
    const stageName = emotion.stage_name?.zh || emotion.dominant_stage;
    document.getElementById('dominantStage').textContent = stageName;
    
    // 恢复阶段
    const phaseName = emotion.phase_name?.zh || emotion.recovery_phase;
    document.getElementById('recoveryPhase').textContent = phaseName;
    
    // 记忆权重
    const weight = emotion.memory_intimacy_weight || 0.5;
    document.getElementById('memoryWeightFill').style.width = `${weight * 100}%`;
    
    // 稳定度
    document.getElementById('stabilityValue').textContent = emotion.stability.toFixed(2);
    
    // 交互次数
    document.getElementById('interactionCount').textContent = emotion.total_interactions;
    
    // 下次主动
    if (emotion.next_proactive_time) {
        const nextTime = new Date(emotion.next_proactive_time);
        const hours = Math.max(0, (nextTime - new Date()) / 3600000);
        document.getElementById('nextProactive').textContent = hours > 0 ? `${hours.toFixed(1)}h` : '已到';
    } else {
        document.getElementById('nextProactive').textContent = '--';
    }
    
    // 安全警报
    const alertEl = document.getElementById('safetyAlert');
    if (emotion.safety_alert) {
        alertEl.classList.remove('hidden');
        document.getElementById('safetyAlertText').textContent = emotion.safety_alert;
    } else {
        alertEl.classList.add('hidden');
    }
    
    // 五阶段分布
    const probs = emotion.stage_probabilities || {};
    document.getElementById('probDenial').style.width = `${(probs.denial || 0.2) * 100}%`;
    document.getElementById('probAnger').style.width = `${(probs.anger || 0.2) * 100}%`;
    document.getElementById('probBargaining').style.width = `${(probs.bargaining || 0.2) * 100}%`;
    document.getElementById('probDepression').style.width = `${(probs.depression || 0.2) * 100}%`;
    document.getElementById('probAcceptance').style.width = `${(probs.acceptance || 0.2) * 100}%`;
}

// ============== Chat Functions ==============

async function loadChat() {
    // 如果没有选中亲人，显示提示
    if (!state.currentProfile) {
        document.getElementById('chatInterface').innerHTML = `
            <div class="empty-state" style="height: 100%;">
                <div class="empty-icon">👥</div>
                <h3>${t('select_loved_one')}</h3>
                <p>${t('select_desc')}</p>
                <button onclick="showPage('profiles')" class="btn-primary">${t('go_select')}</button>
            </div>
        `;
        return;
    }
    
    // 确保聊天界面结构完整（如果之前被替换过）
    if (!document.getElementById('chatName')) {
        location.reload(); // 简单处理：刷新页面恢复结构
        return;
    }
    
    // Set profile info
    const profile = state.currentProfile;
    document.getElementById('chatName').textContent = profile.name;
    const avatar = document.getElementById('chatAvatar');
    if (profile.photo_path) {
        avatar.src = profile.photo_path;
    } else {
        avatar.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="%23e0e7ff"/><text x="50" y="60" text-anchor="middle" font-size="40" fill="%236366f1">👤</text></svg>';
    }
    
    // 更新侧边栏选中状态
    renderChatProfilesList();
    
    // Load history
    try {
        const historyData = await getChatHistory(profile.id);
        renderMessages(historyData.history || []);
    } catch (err) {
        console.error('Failed to load chat history:', err);
        renderMessages([]);
    }
    
    // 如果情感面板打开，更新情感状态
    if (!document.getElementById('emotionPanel').classList.contains('hidden')) {
        loadEmotionState();
    }
}

function renderMessages(messages) {
    const container = document.getElementById('chatMessages');
    container.innerHTML = '';
    
    messages.forEach(msg => {
        addMessageToUI(msg.role, msg.content, msg.created_at);
    });
    
    scrollToBottom();
}

// 追踪已添加的消息，防止重复
const addedMessages = new Set();

function addMessageToUI(role, content, time = null) {
    const container = document.getElementById('chatMessages');
    
    // 生成消息唯一标识（基于角色、内容和当前分钟）
    const messageId = `${role}-${content}-${new Date().getMinutes()}`;
    
    // 检查是否已添加过
    if (addedMessages.has(messageId)) {
        console.log('[addMessageToUI] Duplicate message blocked:', messageId);
        return;
    }
    
    // 记录已添加的消息
    addedMessages.add(messageId);
    
    // 清理旧记录（保留最近50条）
    if (addedMessages.size > 50) {
        const firstKey = addedMessages.values().next().value;
        addedMessages.delete(firstKey);
    }
    
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    
    const avatar = document.createElement('img');
    avatar.className = 'message-avatar';
    if (role === 'user') {
        avatar.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="%23e5e7eb"/><text x="50" y="60" text-anchor="middle" font-size="40" fill="%236b7280">😊</text></svg>';
    } else {
        const profilePhoto = state.currentProfile?.photo_path;
        avatar.src = profilePhoto || 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="%23e0e7ff"/><text x="50" y="60" text-anchor="middle" font-size="40" fill="%236366f1">👤</text></svg>';
    }
    
    const contentWrapper = document.createElement('div');
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = time ? new Date(time).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) : new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    
    contentWrapper.appendChild(contentDiv);
    contentWrapper.appendChild(timeDiv);
    messageEl.appendChild(avatar);
    messageEl.appendChild(contentWrapper);
    container.appendChild(messageEl);
    
    scrollToBottom();
}

function showTypingIndicator() {
    const container = document.getElementById('chatMessages');
    const indicator = document.createElement('div');
    indicator.id = 'typingIndicator';
    indicator.className = 'message assistant';
    const profilePhoto = state.currentProfile?.photo_path;
    indicator.innerHTML = `
        <img class="message-avatar" src="${profilePhoto || 'data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle cx=\"50\" cy=\"50\" r=\"50\" fill=\"%23e0e7ff\"/><text x=\"50\" y=\"60\" text-anchor=\"middle\" font-size=\"40\" fill=\"%236366f1\">👤</text></svg>'}">
        <div>
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    container.appendChild(indicator);
    scrollToBottom();
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

function scrollToBottom() {
    const container = document.getElementById('chatMessages');
    container.scrollTop = container.scrollHeight;
}

// 防止重复发送的标志和消息追踪
let isSending = false;
let lastSentMessage = null;
let lastSentTime = 0;

async function sendMessage() {
    // 防止重复提交
    if (isSending) {
        console.log('[sendMessage] Blocked: already sending');
        return;
    }
    if (!state.currentProfile) {
        console.log('[sendMessage] Blocked: no profile');
        return;
    }
    
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) {
        console.log('[sendMessage] Blocked: empty message');
        return;
    }
    
    // 防止重复发送相同消息（3秒内）
    const now = Date.now();
    if (lastSentMessage === message && (now - lastSentTime) < 3000) {
        console.log('[sendMessage] Blocked: duplicate message');
        return;
    }
    
    // 设置发送中标志
    isSending = true;
    lastSentMessage = message;
    lastSentTime = now;
    
    // 标记是否已处理响应（防止竞态）
    let hasResponded = false;
    
    console.log('[sendMessage] Sending:', message);
    
    // 清空输入框
    input.value = '';
    input.style.height = 'auto';
    
    // 添加用户消息
    addMessageToUI('user', message);
    
    // 显示输入中指示器
    showTypingIndicator();
    
    try {
        // 使用更长的超时（90秒）因为LLM生成需要时间
        const data = await sendChatMessage(state.currentProfile.id, message);
        
        // 如果已经处理过（竞态），则跳过
        if (hasResponded) {
            console.log('[sendMessage] Already responded, skipping duplicate');
            return;
        }
        hasResponded = true;
        
        console.log('[sendMessage] Success:', data.response.substring(0, 50) + '...');
        hideTypingIndicator();
        addMessageToUI('assistant', data.response);
        
        // 更新情感状态显示
        if (data.emotion_state) {
            updateEmotionPanel(data.emotion_state);
        }
    } catch (err) {
        // 如果已经处理过（竞态），则跳过
        if (hasResponded) {
            console.log('[sendMessage] Already responded, skipping error');
            return;
        }
        hasResponded = true;
        
        console.error('[sendMessage] Error:', err);
        hideTypingIndicator();
        
        // 区分超时错误和其他错误
        const errorMsg = err.message && err.message.includes('超时') 
            ? '抱歉，回复时间较长，请稍后再试或直接刷新页面。' 
            : '抱歉，我现在无法回复，请稍后再试。';
        addMessageToUI('assistant', errorMsg);
    } finally {
        // 重置发送标志
        isSending = false;
        console.log('[sendMessage] Reset isSending flag');
    }
}

async function clearCurrentChat() {
    if (!state.currentProfile) return;
    
    if (!confirm('确定要清空与这位亲人的聊天记录吗？')) {
        return;
    }
    
    try {
        showLoading();
        await clearChatHistory(state.currentProfile.id);
        document.getElementById('chatMessages').innerHTML = '';
    } catch (err) {
        alert('清空失败: ' + err.message);
    } finally {
        hideLoading();
    }
}

// ============== Mobile Bottom Navigation ==============

function mobileNavTo(page) {
    console.log('[MobileNav] Navigate to:', page);
    
    // Update active state
    document.querySelectorAll('.nav-item-mobile').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-page') === page) {
            item.classList.add('active');
        }
    });
    
    // Navigate to page
    if (page === 'profiles') {
        showPage('profiles');
    } else if (page === 'chat') {
        // Show chat list page (not directly enter a chat room)
        showChatList();
    } else if (page === 'settings') {
        showSettings();
    }
}

// ============== Chat List Page ==============

function showChatList() {
    console.log('[showChatList] Showing chat list');
    
    // Update nav state
    state.currentPage = 'chatList';
    
    // Hide all pages
    document.getElementById('profilesPage').classList.add('hidden');
    document.getElementById('profileFormPage').classList.add('hidden');
    document.getElementById('chatPage').classList.add('hidden');
    
    // Check if chatList page exists, create if not
    let chatListEl = document.getElementById('chatListPage');
    if (!chatListEl) {
        createChatListPage();
        chatListEl = document.getElementById('chatListPage');
    }
    
    // Show chat list page
    chatListEl.classList.remove('hidden');
    
    // Render chat list
    renderChatListContent();
}

function createChatListPage() {
    const chatListHtml = `
        <div id="chatListPage" class="page hidden">
            <div class="chat-list-container">
                <h2 data-i18n="my_conversations">我的对话</h2>
                <p class="desc" data-i18n="select_chat_desc">选择一个亲人继续对话</p>
                <div id="chatListContent" class="chat-list-content">
                    <!-- Chat list items will be rendered here -->
                </div>
            </div>
        </div>
    `;
    document.querySelector('.content').insertAdjacentHTML('beforeend', chatListHtml);
}

function renderChatListContent() {
    const container = document.getElementById('chatListContent');
    
    if (state.profiles.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">💬</div>
                <h3 data-i18n="no_conversations">暂无对话</h3>
                <p data-i18n="no_conversations_desc">先创建一个亲人档案开始对话吧</p>
                <button onclick="showCreateProfileForm()" class="btn-primary" data-i18n="add_loved_one">添加亲人</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = state.profiles.map(profile => `
        <div class="chat-list-item" onclick="enterChatRoom(${profile.id})">
            <img src="${profile.photo_path || 'data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle cx=\"50\" cy=\"50\" r=\"50\" fill=\"%23e0e7ff\"/><text x=\"50\" y=\"60\" text-anchor=\"middle\" font-size=\"40\" fill=\"%236366f1\">👤</text></svg>'}" 
                 alt="${profile.name}" class="chat-list-avatar">
            <div class="chat-list-info">
                <h3 class="chat-list-name">${profile.name}</h3>
                <p class="chat-list-hint" data-i18n="tap_to_chat">点击开始对话</p>
            </div>
            <span class="chat-list-arrow">›</span>
        </div>
    `).join('');
}

function enterChatRoom(profileId) {
    const profile = state.profiles.find(p => p.id === profileId);
    if (profile) {
        state.currentProfile = profile;
        state.currentProfileId = profileId;
        sessionStorage.setItem('currentProfileId', profileId);
        showPage('chat');
    }
}

// ============== Settings Page ==============

function showSettings() {
    // Simple settings - show language selection and about
    const settingsHtml = `
        <div class="page" id="settingsPage">
            <div class="settings-container">
                <h2 data-i18n="settings">设置</h2>
                <div class="settings-section">
                    <h3 data-i18n="language_settings">语言设置</h3>
                    <select id="settingsUiLanguage" onchange="changeUILanguage(this.value)" class="settings-select">
                        <option value="zh-CN">简体中文</option>
                        <option value="zh-HK">繁體中文（香港）</option>
                        <option value="en">English</option>
                    </select>
                </div>
                <div class="settings-section">
                    <h3 data-i18n="about">关于</h3>
                    <p class="settings-desc">MemorialChat v2.1.0</p>
                    <p class="settings-desc">与思念的人对话</p>
                </div>
                <div class="settings-section">
                    <button onclick="logout()" class="btn-primary btn-logout">退出登录</button>
                </div>
            </div>
        </div>
    `;
    
    // Check if settings page exists
    let settingsEl = document.getElementById('settingsPage');
    if (!settingsEl) {
        document.querySelector('.content').insertAdjacentHTML('beforeend', settingsHtml);
    }
    
    // Hide all pages and show settings
    document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
    document.getElementById('settingsPage').classList.remove('hidden');
    
    // Set current language in settings
    const settingsSelect = document.getElementById('settingsUiLanguage');
    if (settingsSelect) {
        settingsSelect.value = currentUILanguage;
    }
}

// ============== Chat Event Binding ==============

// 全局标志：事件是否已绑定
let eventsBound = false;

function bindChatEvents() {
    if (eventsBound) {
        console.log('[bindChatEvents] Events already bound, skipping');
        return;
    }
    
    console.log('[bindChatEvents] Binding events...');
    
    // Auto-resize textarea
    document.getElementById('messageInput').addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
    
    // Bind send button click
    document.getElementById('sendButton').addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('[sendButton] Clicked');
        sendMessage();
    });
    
    // Bind enter key
    document.getElementById('messageInput').addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) {
            e.preventDefault();
            e.stopPropagation();
            console.log('[messageInput] Enter pressed');
            sendMessage();
        }
    });
    
    eventsBound = true;
    console.log('[bindChatEvents] Events bound successfully');
}

// 绑定事件（只执行一次）
bindChatEvents();

// ============== App Initialization ==============

async function initApp() {
    try {
        showLoading();

        // Initialize UI language
        document.getElementById('uiLanguage').value = currentUILanguage;
        updateAllUIText();

        // Get user info
        const meData = await getMe();
        state.user = meData.user;
        document.getElementById('currentUsername').textContent = state.user.username;

        // Check if user has confirmed consent in this session
        // If not (e.g., page refresh), show consent modal for re-confirmation
        if (!state.hasConfirmedConsentThisSession) {
            showConsentModal();
        } else {
            // User already confirmed consent during this login session
            document.getElementById('authModal').classList.add('hidden');
            document.getElementById('app').classList.remove('hidden');
            document.getElementById('consentModal').classList.add('hidden');

            // Load profiles first
            await loadProfiles();

            // Restore last visited page and selected profile
            const lastPage = sessionStorage.getItem('lastPage') || 'profiles';
            const savedProfileId = sessionStorage.getItem('currentProfileId');
            
            if (savedProfileId && state.profiles.length > 0) {
                const savedProfile = state.profiles.find(p => p.id == savedProfileId);
                if (savedProfile) {
                    state.currentProfile = savedProfile;
                    state.currentProfileId = parseInt(savedProfileId);
                }
            }
            
            // Restore last page (chat or profiles)
            if (lastPage === 'chat' && state.currentProfile) {
                showPage('chat');
            } else {
                showPage('profiles');
            }

            // Check survey status after loading app
            await checkSurveyStatus();
        }
    } catch (err) {
        console.error('Init error:', err);
        logout();
    } finally {
        hideLoading();
    }
}

// Check if already logged in
if (state.token) {
    initApp();
}

// ============== Consent Modal Functions ==============

function showConsentModal() {
    // Hide auth modal and show consent modal
    document.getElementById('authModal').classList.add('hidden');
    document.getElementById('consentModal').classList.remove('hidden');

    // Sync language selector in consent modal with current UI language
    document.getElementById('consentLanguage').value = currentUILanguage;

    // Load consent content based on current language
    loadConsentContent();

    // Reset checkboxes
    document.getElementById('consentRead').checked = false;
    document.getElementById('consentAgree').checked = false;
    document.getElementById('consentWithdraw').checked = false;
    document.getElementById('btnConsentSubmit').disabled = true;

    // Add checkbox listeners
    document.getElementById('consentRead').addEventListener('change', checkConsentCheckboxes);
    document.getElementById('consentAgree').addEventListener('change', checkConsentCheckboxes);
    document.getElementById('consentWithdraw').addEventListener('change', checkConsentCheckboxes);
}

function checkConsentCheckboxes() {
    const allChecked = document.getElementById('consentRead').checked &&
                       document.getElementById('consentAgree').checked &&
                       document.getElementById('consentWithdraw').checked;
    document.getElementById('btnConsentSubmit').disabled = !allChecked;
}

function loadConsentContent() {
    const contentEl = document.getElementById('consentContent');

    const consentContent = {
        'zh-CN': `
            <p>尊敬的用户：</p>
            <p>感谢您使用本渐进式情感支持 AI 聊天机器人（以下简称"本机器人"）。本机器人基于悲伤双过程模型、悲伤五阶段模型、多层情感计算理论研发，专为经历丧亲、丧宠、失恋等情感打击，存在情绪与心理困扰的人群提供非诊疗性的渐进式情感陪伴与心理支持服务，辅助您逐步向心理恢复导向过渡。</p>
            <p>在您使用本机器人服务前，请您仔细阅读本知情同意书，充分理解我们对您个人数据、聊天数据的收集、使用、存储与保护规则，以及您在使用过程中的权利与风险。您勾选"我已阅读并同意"并开始使用本机器人，即视为您已充分理解并自愿同意本知情同意书的全部条款。</p>

            <h3>一、数据收集的目的与用途</h3>
            <p>我们收集您的相关数据仅用于实现本机器人的核心功能、优化服务效果、保障使用安全、开展学术与技术研究，具体用途如下：</p>
            <ol>
                <li>实时抓取您的聊天文本内容、关键词、情感词汇、悲伤相关表述，用于识别您的情绪状态、悲伤五阶段（否认/愤怒/讨价还价/抑郁/接受）归属与变化趋势；</li>
                <li>记录您的交互频率、回复长度、会话节律等行为数据，结合心情指数衰减模型计算您的情感状态，动态调整机器人的回复长度、亲密度、交互频率，实现安全、渐进式的陪伴淡出；</li>
                <li>监测您的情绪强度、风险用语（如自伤、极端消极表述），触发安全预警机制，必要时放缓机器人衰减节奏并提示专业人工心理支持；</li>
                <li>开展匿名化、去标识化的技术优化与学术研究，验证本机器人对悲伤情绪人群的支持效果，提升情感识别与心理支持的准确性；</li>
                <li>构建连续情绪评估与交互熵监控体系，保障服务的安全性与适配性。</li>
            </ol>
            <p>本机器人仅为情感陪伴与心理支持辅助工具，不替代专业心理咨询师、精神科医生的诊断、治疗与医疗服务，数据收集不用于任何商业营销、广告推送或非授权第三方使用。</p>

            <h3>二、我们收集的具体数据类型</h3>
            <p>在您使用本机器人的过程中，我们将自动或手动收集以下数据：</p>
            <ol>
                <li>基础匿名信息：您自主设置的昵称、头像、人设偏好（Partner/Parent/Pet），不强制收集真实姓名、身份证号、联系方式等实名信息；</li>
                <li>聊天交互数据：全部聊天文本内容、聊天关键词、情感词汇密度、悲伤相关表述、回复长度、单次会话时长、交互频率、会话起止时间；</li>
                <li>情感与状态数据：系统计算生成的心情指数、衰减率、悲伤五阶段判别结果、情绪效价/唤醒度、交互熵值、心理状态变化轨迹；</li>
                <li>使用行为数据：机器人回复记录、交互策略调整记录、安全预警触发记录；</li>
                <li>风险监测数据：极端情绪、风险用语的识别与标记数据。</li>
            </ol>

            <h3>三、数据使用与存储规则</h3>
            <ol>
                <li>数据使用范围：您的所有数据仅用于本机器人的功能运行、安全监控、服务优化与合规研究，未经您明确书面同意，绝不会向任何第三方出售、出租、共享或泄露；</li>
                <li>数据存储安全：我们采用加密技术、权限管控、安全服务器存储您的全部数据，严格防范数据泄露、丢失、篡改与非法访问；</li>
                <li>数据存储期限：
                    <ul>
                        <li>您在使用期间，数据将持续存储以保证服务连续性；</li>
                        <li>用于研究的匿名化、去标识化数据，将在研究结束后按学术规范留存或销毁，无法关联到您个人身份；</li>
                    </ul>
                </li>
                <li>数据使用限制：我们不会基于您的心理状态、情绪数据对您进行标签化、歧视性处理，所有数据仅服务于您的个人情感支持需求。</li>
            </ol>

            <h3>四、您的权利</h3>
            <ol>
                <li>知情权：您有权随时查阅本知情同意书、了解自身数据的收集与使用情况；</li>
                <li>访问权：您有权申请查看您的全部聊天数据、情绪状态评估结果、行为记录；</li>
                <li>修改与删除权：您有权修改个人基础信息，随时申请删除全部数据、注销账号；</li>
                <li>撤回同意权：您可随时撤回数据收集使用同意，撤回后我们将立即停止收集新数据，并可按您要求删除已有数据（撤回前基于同意已进行的合法数据使用不受影响）；</li>
                <li>客服咨询权：您可通过平台客服通道，咨询数据相关问题、提出诉求与建议。</li>
            </ol>

            <h3>五、风险提示与免责声明</h3>
            <ol>
                <li>本机器人为非医疗、非诊疗性辅助工具，仅提供情感陪伴与心理支持，不能替代专业心理咨询、心理治疗与医疗干预。若您存在严重心理困扰、自伤自杀倾向或极端情绪，请立即停止使用本机器人，及时联系专业心理机构、医院或身边亲友；</li>
                <li>我们会尽最大努力保障数据安全，但因不可抗力、黑客攻击、网络故障等不可预见因素导致的数据风险，我们将尽力补救但不承担超出合理范围的责任；</li>
                <li>悲伤情绪的变化具有非线性、个体差异性，机器人对您悲伤五阶段的判断、心情指数计算仅为参考，不代表绝对的心理状态诊断；</li>
                <li>当系统监测到您出现持续高强度负向情绪或风险用语时，机器人将自动调整策略并提示人工支持，此为安全辅助机制，不构成医疗建议。</li>
            </ol>

            <h3>六、其他条款</h3>
            <ol>
                <li>我们可能因服务升级、政策调整等原因更新本知情同意书，更新后将在机器人页面显著位置公示，公示后继续使用本机器人即视为同意更新后的条款；</li>
                <li>本知情同意书的解释权归本机器人研发与运营团队所有。</li>
            </ol>

            <h3>确认声明</h3>
            <p>我已仔细阅读、充分理解本知情同意书的全部内容，清楚知晓数据收集的目的、范围、使用规则与自身权利，自愿同意本机器人在服务过程中收集、使用我的相关数据，用于提供渐进式情感陪伴与心理支持服务。</p>
        `,
        'zh-HK': `
            <p>尊敬嘅用戶：</p>
            <p>感謝您使用本漸進式情感支持 AI 聊天機械人（以下簡稱「本機械人」）。本機械人基於悲傷雙過程模型、悲傷五階段模型、多層情感計算理論研發，專為經歷喪親、喪寵、失戀等情感打擊，存在情緒與心理困擾嘅人群提供非診療性嘅漸進式情感陪伴與心理支持服務，輔助您逐步向心理恢復導向過渡。</p>
            <p>喺您使用本機械人服務前，請您仔細閱讀本知情同意書，充分理解我哋對您個人數據、聊天數據嘅收集、使用、存儲與保護規則，以及您喺使用過程中嘅權利與風險。您勾選「我已閱讀並同意」並開始使用本機械人，即視為您已充分理解並自願同意本知情同意書嘅全部條款。</p>

            <h3>一、數據收集嘅目的與用途</h3>
            <p>我哋收集您嘅相關數據僅用於實現本機械人嘅核心功能、優化服務效果、保障使用安全、開展學術與技術研究，具體用途如下：</p>
            <ol>
                <li>實時抓取您嘅聊天文本內容、關鍵詞、情感詞彙、悲傷相關表述，用於識別您嘅情緒狀態、悲傷五階段（否認/憤怒/討價還價/抑郁/接受）歸屬與變化趨勢；</li>
                <li>記錄您嘅交互頻率、回復長度、會話節律等行為數據，結合心情指數衰減模型計算您嘅情感狀態，動態調整機械人嘅回復長度、親密度、交互頻率，實現安全、漸進式嘅陪伴淡出；</li>
                <li>監測您嘅情緒強度、風險用語（如自傷、極端消極表述），觸發安全預警機制，必要時放慢機械人衰減節奏並提示專業人工心理支持；</li>
                <li>開展匿名化、去標識化嘅技術優化與學術研究，驗證本機械人對悲傷情緒人群嘅支持效果，提升情感識別與心理支持嘅準確性；</li>
                <li>構建連續情緒評估與交互熵監控體系，保障服務嘅安全性與適配性。</li>
            </ol>
            <p>本機械人僅為情感陪伴與心理支持輔助工具，不替代專業心理諮詢師、精神科醫生的診斷、治療與醫療服務，數據收集不用於任何商業營銷、廣告推送或非授權第三方使用。</p>

            <h3>二、我哋收集嘅具體數據類型</h3>
            <p>喺您使用本機械人嘅過程中，我哋將自動或手動收集以下數據：</p>
            <ol>
                <li>基礎匿名信息：您自主設置嘅暱稱、頭像、人設偏好（Partner/Parent/Pet），不強制收集真實姓名、身份證號、聯繫方式等實名信息；</li>
                <li>聊天交互數據：全部聊天文本內容、聊天關鍵詞、情感詞彙密度、悲傷相關表述、回復長度、單次會話時長、交互頻率、會話起止時間；</li>
                <li>情感與狀態數據：系統計算生成嘅心情指數、衰減率、悲傷五階段判別結果、情緒效價/喚醒度、交互熵值、心理狀態變化軌跡；</li>
                <li>使用行為數據：機械人回复記錄、交互策略調整記錄、安全預警觸發記錄；</li>
                <li>風險監測數據：極端情緒、風險用語嘅識別與標記數據。</li>
            </ol>

            <h3>三、數據使用與存儲規則</h3>
            <ol>
                <li>數據使用範圍：您嘅所有數據僅用於本機械人嘅功能運行、安全監控、服務優化與合規研究，未經您明確書面同意，絕不會向任何第三方出售、出租、共享或洩露；</li>
                <li>數據存儲安全：我哋採用加密技術、權限管控、安全服務器存儲您嘅全部數據，嚴格防範數據洩露、丟失、篡改與非法訪問；</li>
                <li>數據存儲期限：
                    <ul>
                        <li>您喺使用期間，數據將持續存儲以保證服務連續性；</li>
                        <li>用於研究嘅匿名化、去標識化數據，將在研究結束後按學術規範留存或銷毀，無法關聯到您個人身份；</li>
                    </ul>
                </li>
                <li>數據使用限制：我哋唔會基於您嘅心理狀態、情緒數據對您進行標籤化、歧視性處理，所有數據僅服務於您嘅個人情感支持需求。</li>
            </ol>

            <h3>四、您嘅權利</h3>
            <ol>
                <li>知情權：您有權隨時查閱本知情同意書、了解自身數據嘅收集與使用情況；</li>
                <li>訪問權：您有權申請查看您嘅全部聊天數據、情緒狀態評估結果、行為記錄；</li>
                <li>修改與刪除權：您有權修改個人基礎信息，隨時申請刪除全部數據、註銷賬號；</li>
                <li>撤回同意權：您可隨時撤回數據收集使用同意，撤回後我哋將立即停止收集新數據，並可按您要求刪除已有數據（撤回前基於同意已進行嘅合法數據使用不受影響）；</li>
                <li>客服諮詢權：您可通過平台客服通道，諮詢數據相關問題、提出訴求與建議。</li>
            </ol>

            <h3>五、風險提示與免責聲明</h3>
            <ol>
                <li>本機械人為非醫療、非診療性輔助工具，僅提供情感陪伴與心理支持，不能替代專業心理諮詢、心理治療與醫療干預。若您存在嚴重心理困擾、自傷自殺傾向或極端情緒，請立即停止使用本機械人，及時聯繫專業心理機構、醫院或身邊親友；</li>
                <li>我哋會盡最大努力保障數據安全，但因不可抗力、黑客攻擊、網絡故障等不可預見因素導致嘅數據風險，我哋將盡力補救但唔承擔超出合理範圍嘅責任；</li>
                <li>悲傷情緒嘅變化具有非線性、個體差異性，機械人對您悲傷五階段嘅判斷、心情指數計算僅為參考，唔代表絕對嘅心理狀態診斷；</li>
                <li>當系統監測到您出現持續高強度負向情緒或風險用語時，機械人將自動調整策略並提示人工支持，此為安全輔助機制，不構成醫療建議。</li>
            </ol>

            <h3>六、其他條款</h3>
            <ol>
                <li>我哋可能因服務升級、政策調整等原因更新本知情同意書，更新後將喺機械人頁面顯著位置公示，公示後繼續使用本機械人即視為同意更新後嘅條款；</li>
                <li>本知情同意書嘅解釋權歸本機械人研發與運營團隊所有。</li>
            </ol>

            <h3>確認聲明</h3>
            <p>我已仔細閱讀、充分理解本知情同意書嘅全部內容，清楚知曉數據收集嘅目的、範圍、使用規則與自身權利，自願同意本機械人喺服務過程中收集、使用我嘅相關數據，用於提供漸進式情感陪伴與心理支持服務。</p>
        `,
        'en': `
            <p>Dear User,</p>
            <p>Thank you for using this Progressive Emotional Support AI Chatbot (hereinafter referred to as the "Chatbot"). This Chatbot is developed based on the Dual Process Model of Grief, Five Stages of Grief Model, and Multi-layer Emotional Computing Theory. It provides non-clinical progressive emotional companionship and psychological support services for people experiencing emotional shocks such as bereavement, pet loss, or breakup, and who have emotional and psychological distress, assisting you in gradually transitioning toward psychological recovery.</p>
            <p>Before you use the Chatbot services, please carefully read this Informed Consent Form to fully understand our rules regarding the collection, use, storage, and protection of your personal data and chat data, as well as your rights and risks during use. By checking "I have read and agree" and starting to use the Chatbot, you are deemed to have fully understood and voluntarily agreed to all terms of this Informed Consent Form.</p>

            <h3>I. Purpose and Use of Data Collection</h3>
            <p>We collect your relevant data solely for implementing the Chatbot's core functions, optimizing service effectiveness, ensuring usage safety, and conducting academic and technical research. The specific purposes are as follows:</p>
            <ol>
                <li>To capture your chat text content, keywords, emotional vocabulary, and grief-related expressions in real-time for identifying your emotional state, Five Stages of Grief (Denial/Anger/Bargaining/Depression/Acceptance) classification, and changing trends;</li>
                <li>To record your behavioral data such as interaction frequency, reply length, and session rhythm, combined with the Mood Index Decay Model to calculate your emotional state, dynamically adjusting the Chatbot's reply length, intimacy, and interaction frequency to achieve safe, progressive companionship fade-out;</li>
                <li>To monitor your emotional intensity and risky language (such as self-harm or extreme negative expressions), trigger safety warning mechanisms, and when necessary, slow down the Chatbot's decay rhythm and suggest professional human psychological support;</li>
                <li>To conduct anonymized and de-identified technical optimization and academic research, verifying the Chatbot's support effectiveness for people with grief emotions, and improving the accuracy of emotional recognition and psychological support;</li>
                <li>To build a continuous emotion assessment and interaction entropy monitoring system to ensure service safety and adaptability.</li>
            </ol>
            <p>This Chatbot is solely an emotional companionship and psychological support auxiliary tool and does not replace the diagnosis, treatment, and medical services of professional psychological counselors or psychiatrists. Data collection is not used for any commercial marketing, advertising push, or unauthorized third-party use.</p>

            <h3>II. Specific Data Types We Collect</h3>
            <p>During your use of the Chatbot, we will automatically or manually collect the following data:</p>
            <ol>
                <li>Basic Anonymous Information: Nickname, avatar, and persona preference (Partner/Parent/Pet) that you voluntarily set. We do not require collection of real-name information such as real name, ID number, or contact details;</li>
                <li>Chat Interaction Data: All chat text content, chat keywords, emotional vocabulary density, grief-related expressions, reply length, single session duration, interaction frequency, and session start/end times;</li>
                <li>Emotional and State Data: Mood index, decay rate, Five Stages of Grief classification results, emotional valence/arousal, interaction entropy value, and psychological state change trajectory calculated by the system;</li>
                <li>Usage Behavior Data: Chatbot reply records, interaction strategy adjustment records, and safety warning trigger records;</li>
                <li>Risk Monitoring Data: Identification and marking data for extreme emotions and risky language.</li>
            </ol>

            <h3>III. Data Use and Storage Rules</h3>
            <ol>
                <li>Scope of Data Use: All your data is used solely for the Chatbot's functional operation, security monitoring, service optimization, and compliance research. Without your explicit written consent, we will absolutely not sell, rent, share, or disclose your data to any third party;</li>
                <li>Data Storage Security: We use encryption technology, access control, and secure servers to store all your data, strictly preventing data leaks, loss, tampering, and unauthorized access;</li>
                <li>Data Storage Period:
                    <ul>
                        <li>During your use, data will be continuously stored to ensure service continuity;</li>
                        <li>Anonymized and de-identified data used for research will be retained or destroyed according to academic standards after the research ends, and cannot be linked to your personal identity;</li>
                    </ul>
                </li>
                <li>Data Use Restrictions: We will not label or discriminate against you based on your psychological state or emotional data. All data serves solely your personal emotional support needs.</li>
            </ol>

            <h3>IV. Your Rights</h3>
            <ol>
                <li>Right to Know: You have the right to review this Informed Consent Form and understand the collection and use of your data at any time;</li>
                <li>Right of Access: You have the right to apply to view all your chat data, emotional state assessment results, and behavioral records;</li>
                <li>Right to Modification and Deletion: You have the right to modify your personal basic information and apply to delete all data and cancel your account at any time;</li>
                <li>Right to Withdraw Consent: You may withdraw your consent to data collection and use at any time. After withdrawal, we will immediately stop collecting new data and may delete existing data upon your request (legal data use based on consent before withdrawal is not affected);</li>
                <li>Right to Customer Service Consultation: You may consult data-related questions and submit requests and suggestions through the platform's customer service channel.</li>
            </ol>

            <h3>V. Risk Warnings and Disclaimer</h3>
            <ol>
                <li>This Chatbot is a non-medical, non-clinical auxiliary tool that provides only emotional companionship and psychological support and cannot replace professional psychological counseling, psychotherapy, or medical intervention. If you have severe psychological distress, self-harm or suicidal tendencies, or extreme emotions, please stop using the Chatbot immediately and contact professional psychological institutions, hospitals, or relatives and friends around you in a timely manner;</li>
                <li>We will make our best efforts to ensure data security, but for data risks caused by unforeseen factors such as force majeure, hacker attacks, or network failures, we will try our best to remedy but will not bear responsibilities beyond a reasonable scope;</li>
                <li>Changes in grief emotions are non-linear and individually different. The Chatbot's judgment of your Five Stages of Grief and mood index calculations are for reference only and do not represent an absolute psychological state diagnosis;</li>
                <li>When the system detects that you have continuous high-intensity negative emotions or risky language, the Chatbot will automatically adjust its strategy and suggest human support. This is a safety assistance mechanism and does not constitute medical advice.</li>
            </ol>

            <h3>VI. Other Terms</h3>
            <ol>
                <li>We may update this Informed Consent Form due to service upgrades, policy adjustments, or other reasons. After updates, it will be prominently displayed on the Chatbot page. Continuing to use the Chatbot after the announcement is deemed as agreeing to the updated terms;</li>
                <li>The right to interpret this Informed Consent Form belongs to the Chatbot's development and operation team.</li>
            </ol>

            <h3>Confirmation Statement</h3>
            <p>I have carefully read and fully understood all the contents of this Informed Consent Form, clearly understand the purpose, scope, and rules of use of data collection and my rights, and voluntarily agree that the Chatbot may collect and use my relevant data during the service to provide progressive emotional companionship and psychological support services.</p>
        `
    };

    contentEl.innerHTML = consentContent[currentUILanguage] || consentContent['zh-CN'];
}

async function submitConsent() {
    try {
        showLoading();
        await updateConsent(true);
        // Mark consent as confirmed in this session
        state.hasConfirmedConsentThisSession = true;
        document.getElementById('consentModal').classList.add('hidden');
        document.getElementById('app').classList.remove('hidden');

        // Load profiles and show app
        await loadProfiles();
        showPage('profiles');

        // Check survey status after consent
        await checkSurveyStatus();
    } catch (err) {
        alert('保存同意失败：' + err.message);
    } finally {
        hideLoading();
    }
}

// ============== Survey Modal Functions ==============

function showSurveyModal() {
    // Show survey modal
    document.getElementById('surveyModal').classList.remove('hidden');

    // Sync language selector in survey modal with current UI language
    document.getElementById('surveyLanguage').value = currentUILanguage;
}

async function checkSurveyStatus() {
    try {
        // First check local storage for quick check
        const localLastSurvey = localStorage.getItem('lastSurveyDate');

        if (localLastSurvey) {
            state.lastSurveyDate = localLastSurvey;
            const lastDate = new Date(localLastSurvey);
            const now = new Date();
            const diffDays = Math.floor((now - lastDate) / (1000 * 60 * 60 * 24));

            if (diffDays >= 5) {
                // Survey is due, show it
                state.surveyDue = true;
                showSurveyModal();
                return;
            }
        }

        // Check server status
        const surveyStatus = await getSurveyStatus();
        if (surveyStatus.survey_due) {
            state.surveyDue = true;
            state.lastSurveyDate = surveyStatus.last_survey_date;
            showSurveyModal();
        }
    } catch (err) {
        console.error('Check survey status error:', err);
        // If server check fails, use local check
        const localLastSurvey = localStorage.getItem('lastSurveyDate');
        if (localLastSurvey) {
            const lastDate = new Date(localLastSurvey);
            const now = new Date();
            const diffDays = Math.floor((now - lastDate) / (1000 * 60 * 60 * 24));
            if (diffDays >= 5) {
                state.surveyDue = true;
                showSurveyModal();
            }
        }
    }
}

async function submitSurvey() {
    // Get form values
    const form = document.getElementById('surveyForm');
    const formData = new FormData(form);

    // Validate all questions are answered
    const requiredQuestions = ['q1', 'q2', 'q3', 'q4', 'q5'];
    for (const q of requiredQuestions) {
        if (!formData.get(q)) {
            alert(`请回答问题 ${q.replace('q', '')}`);
            return;
        }
    }

    // Collect answers
    const answers = {
        mood_today: parseInt(formData.get('q1')),
        emotion_intensity: parseInt(formData.get('q2')),
        dual_process_state: parseInt(formData.get('q3')),
        five_stage_state: parseInt(formData.get('q4')),
        companionship_preference: parseInt(formData.get('q5'))
    };

    try {
        showLoading();
        await submitSurveyData(answers);

        // Save last survey date
        const now = new Date();
        state.lastSurveyDate = now.toISOString();
        localStorage.setItem('lastSurveyDate', now.toISOString());
        state.surveyDue = false;

        document.getElementById('surveyModal').classList.add('hidden');
        alert('问卷提交成功！');
    } catch (err) {
        alert('问卷提交失败：' + err.message);
    } finally {
        hideLoading();
    }
}
