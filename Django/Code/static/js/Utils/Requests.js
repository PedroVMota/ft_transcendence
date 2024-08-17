class Requests {
    static async get(url, headers = {}) {
        return this.#makeRequest('GET', url, headers);
    }

    static async post(url, data = {}, headers = {}) {
        return this.#makeRequest('POST', url, headers, data);
    }

    static async put(url, data = {}, headers = {}) {
        return this.#makeRequest('PUT', url, headers, data);
    }

    static async delete(url, headers = {}) {
        return this.#makeRequest('DELETE', url, headers);
    }

    static async #makeRequest(method, url, headers = {}, data = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                ...headers,
            },
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {
                return await response.json(); // Return JSON if response is JSON
            } else {
                return await response.text(); // Return text for other types
            }
        } catch (error) {
            console.error("Request failed", error);
            throw error;
        }
    }
}

export default Requests;