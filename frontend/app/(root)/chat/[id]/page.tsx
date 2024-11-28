import { PageContent } from "@/components/page-content";

export interface ChatPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function ChatPage({ params }: ChatPageProps) {
  // Cast params to the expected type
  const { id } = await params;

  return <PageContent id={id} />;
}
