package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"time"
	"bytes"
)

type QuickbaseAPI struct {
	Realm     string
	UserToken string
	AppToken  string
	BaseURL   string
}

func NewQuickbaseAPI(realm, userToken, appToken string) *QuickbaseAPI {
	return &QuickbaseAPI{
		Realm:     realm,
		UserToken: userToken,
		AppToken:  appToken,
		BaseURL:   "https://api.quickbase.com/v1",
	}
}

func (qb *QuickbaseAPI) getAuthHeaders() map[string]string {
	timestamp := fmt.Sprintf("%d", time.Now().Unix())
	nonce := base64.StdEncoding.EncodeToString([]byte(time.Now().String()))

	// Create signature string
	signatureString := fmt.Sprintf("%s&%s&%s", qb.UserToken, timestamp, nonce)

	// Generate HMAC signature
	h := hmac.New(sha256.New, []byte(qb.AppToken))
	h.Write([]byte(signatureString))
	signature := fmt.Sprintf("%x", h.Sum(nil))

	return map[string]string{
		"QB-Realm-Hostname": qb.Realm,
		"Authorization":     fmt.Sprintf("QB-USER-TOKEN %s", qb.UserToken),
		"QB-Timestamp":      timestamp,
		"QB-Nonce":          nonce,
		"QB-Signature":      signature,
		"Content-Type":      "application/json",
	}
}

func (qb *QuickbaseAPI) QueryRecords(tableID string, query []int) (map[string]interface{}, error) {
	endpoint := fmt.Sprintf("%s/records/query", qb.BaseURL)

	payload := map[string]interface{}{
		"from":   tableID,
		"select": query,
	}

	jsonData, err := json.Marshal(payload)
	if err != nil {
		return nil, fmt.Errorf("error marshaling payload: %v", err)
	}

	req, err := http.NewRequest("POST", endpoint, bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("error creating request: %v", err)
	}

	// Add headers
	headers := qb.getAuthHeaders()
	for key, value := range headers {
		req.Header.Add(key, value)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("error making request: %v", err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("error reading response: %v", err)
	}

	var result map[string]interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("error parsing response: %v", err)
	}

	return result, nil
}

func main() {
	// Replace these with your actual credentials
	realm := "your-realm.quickbase.com"
	userToken := "your-user-token"
	appToken := "your-app-token"

	// Initialize the API client
	qb := NewQuickbaseAPI(realm, userToken, appToken)

	// Example query
	tableID := "bqxxxxx" // Replace with your table ID
	query := []int{1, 2, 3} // Replace with your field IDs

	result, err := qb.QueryRecords(tableID, query)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Pretty print the result
	jsonResult, _ := json.MarshalIndent(result, "", "  ")
	fmt.Println(string(jsonResult))
} 