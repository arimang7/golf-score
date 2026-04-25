import axios from 'axios';

// VITE_API_URL 환경 변수가 있으면 그것을 사용하고, 
// 프로덕션 빌드일 때는 상대 경로('/api'나 그냥 '/')를 사용할 수 있습니다.
// 여기서는 Vercel 환경에서 백엔드가 동일 도메인의 루트를 사용하도록 설정합니다.
const baseURL = import.meta.env.PROD ? '' : 'http://localhost:8000';

const api = axios.create({
  baseURL: baseURL,
  withCredentials: true,
});

export default api;
