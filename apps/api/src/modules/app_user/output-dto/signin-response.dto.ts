import { ApiProperty } from '@nestjs/swagger';

export class SigninResponseDto {
  @ApiProperty({ description: 'ISO timestamp' })
  expiresAt!: string;
}
