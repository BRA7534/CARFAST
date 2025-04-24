import Foundation
import shared

@MainActor
class SearchViewModel: ObservableObject {
    private let searchApi: SearchApi
    
    @Published var searchState: SearchState = .initial
    @Published var savedSearches: [SavedSearch] = []
    
    init(searchApi: SearchApi) {
        self.searchApi = searchApi
        loadSavedSearches()
    }
    
    func search(params: SearchParams) async {
        searchState = .loading
        
        do {
            let result = try await searchApi.searchVehicles(params: params)
            searchState = .success(result)
        } catch {
            searchState = .error(error.localizedDescription)
        }
    }
    
    func saveSearch(params: SearchParams, name: String) async {
        do {
            _ = try await searchApi.saveSearch(params: params, name: name)
            await loadSavedSearches()
        } catch {
            // Handle error
        }
    }
    
    private func loadSavedSearches() async {
        do {
            savedSearches = try await searchApi.getSavedSearches()
        } catch {
            // Handle error
        }
    }
}

enum SearchState {
    case initial
    case loading
    case success(SearchResult)
    case error(String)
}
