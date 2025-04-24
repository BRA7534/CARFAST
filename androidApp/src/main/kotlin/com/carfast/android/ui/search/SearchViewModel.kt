package com.carfast.android.ui.search

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.carfast.api.SearchApi
import com.carfast.models.SearchParams
import com.carfast.models.SearchResult
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class SearchViewModel(
    private val searchApi: SearchApi
) : ViewModel() {
    private val _searchState = MutableStateFlow<SearchState>(SearchState.Initial)
    val searchState: StateFlow<SearchState> = _searchState
    
    private val _savedSearches = MutableStateFlow<List<SavedSearch>>(emptyList())
    val savedSearches: StateFlow<List<SavedSearch>> = _savedSearches
    
    init {
        loadSavedSearches()
    }
    
    fun search(params: SearchParams) {
        viewModelScope.launch {
            try {
                _searchState.value = SearchState.Loading
                val result = searchApi.searchVehicles(params)
                _searchState.value = SearchState.Success(result)
            } catch (e: Exception) {
                _searchState.value = SearchState.Error(e.message ?: "Erreur de recherche")
            }
        }
    }
    
    fun saveSearch(params: SearchParams, name: String) {
        viewModelScope.launch {
            try {
                searchApi.saveSearch(params, name)
                loadSavedSearches()
            } catch (e: Exception) {
                // Gérer l'erreur
            }
        }
    }
    
    private fun loadSavedSearches() {
        viewModelScope.launch {
            try {
                _savedSearches.value = searchApi.getSavedSearches()
            } catch (e: Exception) {
                // Gérer l'erreur
            }
        }
    }
}

sealed class SearchState {
    object Initial : SearchState()
    object Loading : SearchState()
    data class Success(val result: SearchResult) : SearchState()
    data class Error(val message: String) : SearchState()
}
