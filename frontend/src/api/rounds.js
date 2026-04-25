import api from './client';

export const createRound = async (data) => {
  const response = await api.post('/rounds/', data);
  return response.data;
};

export const getRound = async (id) => {
  const response = await api.get(`/rounds/${id}`);
  return response.data;
};

export const listRounds = async () => {
  const response = await api.get('/rounds/');
  return response.data;
};

export const updateHoleScore = async (roundId, holeNumber, scores, par) => {
  const params = par !== undefined ? { par } : {};
  const response = await api.patch(`/rounds/${roundId}/holes/${holeNumber}`, scores, { params });
  return response.data;
};

export const uploadVoice = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/voice/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const parseVoiceText = async (text, parHint) => {
  const params = parHint !== undefined ? { par_hint: parHint } : {};
  const response = await api.post('/voice/parse', { text }, { params });
  return response.data;
};
