function resolveApiBase() {
  if (window.MSAHOO2007_API) return window.MSAHOO2007_API;
  if (window.location.port === '5000') {
    return `${window.location.origin}/api`;
  }
  return 'http://127.0.0.1:5000/api';
}

const API_BASE = resolveApiBase();
class MSahoo2007API {
  constructor(baseUrl = API_BASE) {
    this.baseUrl = baseUrl;
    this.token = localStorage.getItem('msahoo2007_token') || null;
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('msahoo2007_token', token);
    } else {
      localStorage.removeItem('msahoo2007_token');
    }
  }

  async request(endpoint, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.error || data.message || 'Request failed');
    }

    return data;
  }

  async register(name, email, password) {
    const data = await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password }),
    });
    this.setToken(data.token);
    return data;
  }

  async login(email, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    this.setToken(data.token);
    return data;
  }

  logout() {
    this.setToken(null);
  }

  async submitContact(formData) {
    return this.request('/contact', {
      method: 'POST',
      body: JSON.stringify(formData),
    });
  }

  async getAdminStats() {
    return this.request('/admin/stats');
  }

  async getAdminContacts() {
    return this.request('/admin/contacts');
  }

  async subscribeNewsletter(email) {
    return this.request('/newsletter', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  }

  async getBlogs(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/blogs${query ? `?${query}` : ''}`);
  }

  async getBlog(id) {
    return this.request(`/blogs/${id}`);
  }

  async getProjects(category = '') {
    const query = category && category !== 'all' ? `?category=${encodeURIComponent(category)}` : '';
    return this.request(`/projects${query}`);
  }

  async getProject(id) {
    return this.request(`/projects/${id}`);
  }
}

window.msahooAPI = new MSahoo2007API();
