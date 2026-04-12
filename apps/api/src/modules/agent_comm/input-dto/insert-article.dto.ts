import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { z } from 'zod';

export class InsertArticleDto {
  static schema = z.object({
    title: z.string().trim().min(1).max(500),
    url: z.string().url().max(1000),
    content_raw: z.string().trim().min(1),
    published_at: z.string().datetime(),
    source_name: z.string().trim().min(1).max(200),
    source_type: z.enum(['RSS', 'BLOG', 'NEWS', 'SOCIAL', 'PAPER', 'NEWSLETTER', 'COMMUNITY', 'OFFICIAL']).default('RSS'),
    language: z.string().max(10).optional(),
    author: z.string().max(255).optional(),
  });

  @ApiProperty({ example: 'GPT-5 Released with Major Performance Gains' })
  title!: string;

  @ApiProperty({ example: 'https://techblog.example.com/gpt-5-released' })
  url!: string;

  @ApiProperty({ example: 'OpenAI has announced GPT-5 with significant improvements...' })
  content_raw!: string;

  @ApiProperty({ example: '2026-04-12T09:00:00Z' })
  published_at!: string;

  @ApiProperty({ example: 'Tech Blog', description: '소스 이름 (없으면 자동 생성)' })
  source_name!: string;

  @ApiPropertyOptional({
    example: 'RSS',
    enum: ['RSS', 'BLOG', 'NEWS', 'SOCIAL', 'PAPER', 'NEWSLETTER', 'COMMUNITY', 'OFFICIAL'],
    default: 'RSS',
  })
  source_type?: string;

  @ApiPropertyOptional({ example: 'en' })
  language?: string;

  @ApiPropertyOptional({ example: 'John Doe' })
  author?: string;
}
