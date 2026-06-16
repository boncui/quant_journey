import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api/client";

export function useCatalog() {
  return useQuery({
    queryKey: ["catalog"],
    queryFn: async () => {
      const { data, error } = await api.GET("/api/v1/catalog", {});
      if (error || !data) throw error ?? new Error("no catalog");
      return data;
    },
  });
}
