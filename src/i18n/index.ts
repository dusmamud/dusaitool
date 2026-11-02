export const DEFAULT_LOCALE = 'en-IN' as const;
export type Locale = 'en-IN' | 'hi';

export const LOCALES: { code: Locale; label: string; nativeLabel: string; path: string; htmlLang: string }[] = [
  { code: 'en-IN', label: 'English (India)', nativeLabel: 'English', path: '', htmlLang: 'en-IN' },
  { code: 'hi', label: 'Hindi', nativeLabel: 'हिन्दी', path: 'hi', htmlLang: 'hi' },
];

const ui = {
  'en-IN': {
    home: 'Home',
    blog: 'Blog',
    search: 'Search',
    tagline: 'AI tools, tested in India — free or paid, in rupees, with Hindi support.',
    latest: 'Latest tested tools',
    testedThisWeek: 'Tested this week',
    toolsTested: 'tools tested',
    browseTools: 'Browse tested tools',
    searchTools: 'Search tools',
    allPosts: 'All posts',
    tags: 'Topics',
    contents: 'On this page',
    related: 'Related guides',
    searchResults: 'results',
    searchNoResults: 'No results for that search. Try a shorter word, or browse a topic below.',
    popularSearches: 'Popular searches',
    goHome: 'Go to home page',
    suggested: 'Suggested pages',
    readMore: 'Read more',
    readTime: 'min read',
    updated: 'Updated',
    published: 'Published',
    backToBlog: 'Back to blog',
    searchPlaceholder: 'Search tools, tutorials, comparisons…',
    searchHint: 'Search is built at deploy time. No data leaves your browser.',
    searching: 'Searching…',
    searchNoIndex: 'Search index is not built yet. Run npm run build first.',
    noPosts: 'No posts in this language yet.',
    skip: 'Skip to main content',
    themeLight: 'Switch to light theme',
    themeDark: 'Switch to dark theme',
    language: 'Language',
    footerNote: 'Every tool on this site is tested by hand before it is recommended. Prices change — check the official page before you pay.',
    legal: 'Legal',
    privacyPolicy: 'Privacy Policy',
    termsConditions: 'Terms and Conditions',
    disclaimer: 'Disclaimer',
  },
  hi: {
    home: 'होम',
    blog: 'ब्लॉग',
    search: 'खोजें',
    tagline: 'भारत में टेस्ट किए गए AI टूल — फ्री या पेड, रुपये में कीमत, हिंदी सपोर्ट के साथ।',
    latest: 'नवीनतम टेस्ट किए गए टूल',
    testedThisWeek: 'इस हफ्ते टेस्ट किया गया',
    toolsTested: 'टूल टेस्ट किए गए',
    browseTools: 'टेस्ट किए गए टूल देखें',
    searchTools: 'टूल खोजें',
    allPosts: 'सभी पोस्ट',
    tags: 'विषय',
    contents: 'इस पेज पर',
    related: 'संबंधित गाइड',
    searchResults: 'परिणाम',
    searchNoResults: 'इस खोज के लिए कोई परिणाम नहीं है। छोटा शब्द आज़माएं, या नीचे कोई विषय चुनें।',
    popularSearches: 'लोकप्रिय खोजें',
    goHome: 'होम पेज पर जाएं',
    suggested: 'सुझाए गए पेज',
    readMore: 'और पढ़ें',
    readTime: 'मिनट पढ़ें',
    updated: 'अपडेट',
    published: 'प्रकाशित',
    backToBlog: 'ब्लॉग पर वापस जाएं',
    searchPlaceholder: 'टूल, ट्यूटोरियल, तुलना खोजें…',
    searchHint: 'खोज डिप्लॉय के समय बनती है। आपका डेटा ब्राउज़र से बाहर नहीं जाता।',
    searching: 'खोज रहे हैं…',
    searchNoIndex: 'खोज इंडेक्स अभी बना नहीं है। पहले npm run build चलाएं।',
    noPosts: 'इस भाषा में अभी कोई पोस्ट नहीं है।',
    skip: 'मुख्य सामग्री पर जाएं',
    themeLight: 'लाइट थीम पर जाएं',
    themeDark: 'डार्क थीम पर जाएं',
    language: 'भाषा',
    footerNote: 'इस साइट पर हर टूल को सिफारिश से पहले हाथ से टेस्ट किया जाता है। कीमतें बदलती रहती हैं — भुगतान से पहले आधिकारिक पेज देखें।',
    legal: 'कानूनी',
    privacyPolicy: 'गोपनीयता नीति',
    termsConditions: 'नियम और शर्तें',
    disclaimer: 'अस्वीकरण',
  },
} satisfies Record<Locale, Record<string, string>>;

export function t(locale: Locale, key: keyof (typeof ui)['en-IN']): string {
  return ui[locale][key] ?? ui['en-IN'][key];
}

export function localeFromPath(pathname: string): Locale {
  return pathname.startsWith('/hi/') || pathname === '/hi' ? 'hi' : 'en-IN';
}

/** Build the same page in another locale. English has no prefix. */
export function localizePath(pathname: string, target: Locale): string {
  const withoutHi = pathname.replace(/^\/hi(?=\/|$)/, '') || '/';
  if (target === 'hi') return withoutHi === '/' ? '/hi/' : `/hi${withoutHi}`;
  return withoutHi;
}

export function otherLocale(locale: Locale): Locale {
  return locale === 'en-IN' ? 'hi' : 'en-IN';
}

/** Slug without the locale folder, e.g. "en-IN/a-b" -> "a-b". */
export function slugFromId(id: string): string {
  return id.replace(/^(en-in|hi)\//i, '').replace(/\.(md|mdx)$/, '');
}

export function readingMinutes(body: string): number {
  const words = body.replace(/[#>*`[\]()!]/g, ' ').split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 200));
}
