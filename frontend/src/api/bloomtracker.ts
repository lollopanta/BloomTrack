import { apiClient } from './client';
import { ApiResponse, DatasetData, PredictionData } from '../types';

/**
 * BloomTracker API functions for data and prediction endpoints
 */

// Dataset Data Functions
export const getDatasetData = async (dataset: string): Promise<ApiResponse<DatasetData>> => {
  try {
    const response = await apiClient.get(`/data/${dataset}`);
    return response.data;
  } catch (error: any) {
    console.error(`Error fetching ${dataset} data:`, error);
    throw new Error(`Failed to fetch ${dataset} data: ${error.message}`);
  }
};

export const getAllDatasetData = async (): Promise<ApiResponse<Record<string, DatasetData>>> => {
  try {
    const response = await apiClient.get('/data/all');
    return response.data;
  } catch (error: any) {
    console.error('Error fetching all dataset data:', error);
    throw new Error(`Failed to fetch all dataset data: ${error.message}`);
  }
};

// Prediction Functions
export const getPredictions = async (
  dataset: string, 
  model: string = 'auto'
): Promise<ApiResponse<PredictionData>> => {
  try {
    const response = await apiClient.get(`/predict/${dataset}?model=${model}`);
    return response.data;
  } catch (error: any) {
    console.error(`Error fetching ${dataset} predictions:`, error);
    throw new Error(`Failed to fetch ${dataset} predictions: ${error.message}`);
  }
};

export const getAllPredictions = async (
  model: string = 'auto'
): Promise<ApiResponse<Record<string, PredictionData>>> => {
  try {
    const response = await apiClient.get(`/predict/all?model=${model}`);
    return response.data;
  } catch (error: any) {
    console.error('Error fetching all predictions:', error);
    throw new Error(`Failed to fetch all predictions: ${error.message}`);
  }
};

// Model Management Functions
export const trainModel = async (
  dataset: string, 
  model: string = 'auto'
): Promise<ApiResponse> => {
  try {
    const response = await apiClient.post(`/predict/train?dataset=${dataset}&model=${model}`);
    return response.data;
  } catch (error: any) {
    console.error(`Error training ${model} model for ${dataset}:`, error);
    throw new Error(`Failed to train model: ${error.message}`);
  }
};

export const getModels = async (): Promise<ApiResponse> => {
  try {
    const response = await apiClient.get('/predict/models');
    return response.data;
  } catch (error: any) {
    console.error('Error fetching models:', error);
    throw new Error(`Failed to fetch models: ${error.message}`);
  }
};

// Health Check
export const getHealthStatus = async (): Promise<ApiResponse> => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error: any) {
    console.error('Error checking health status:', error);
    throw new Error(`Failed to check health status: ${error.message}`);
  }
};

// API Info
export const getApiInfo = async (): Promise<ApiResponse> => {
  try {
    const response = await apiClient.get('/');
    return response.data;
  } catch (error: any) {
    console.error('Error fetching API info:', error);
    throw new Error(`Failed to fetch API info: ${error.message}`);
  }
};
